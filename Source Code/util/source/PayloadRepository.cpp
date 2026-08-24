/*
 * PIZZA HEN R7.4 - Payload Repository service subset.
 *
 * Source authority: ps5-payload-manager 0.5.1 repository.c/json_helpers.c/
 * sha256.c supplied by the user.  Only repository parsing/download/checksum
 * behavior is retained.  PLDMGR's HTTP server, launcher app, settings, stats,
 * history, USB import and full frontend are intentionally NOT integrated.
 *
 * PIZZA adaptation requested by the project:
 *   storage = /data/PIZZA_HEN/payloads/<filename>
 *   repo UI = existing PIZZA HEN Toolbox
 *   launch/stop/autostart = existing PIZZA HEN PluginManager
 */
#include <payload_repository.hpp>
#include <pizzahen_payloads_builtin.hpp>
#include <plugin_manager.hpp>
extern "C" {
#include "common_utils.h"
#include "pldmgr_sha256.h"
}
#include <cctype>
#include <cerrno>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <strings.h>
#include <fcntl.h>
#include <string>
#include <sys/stat.h>
#include <unistd.h>
#include <vector>

namespace {
constexpr const char *kRepoSource = "builtin://PIZZA_HEN/payloads.json";
constexpr const char *kSourceCache = "/data/PIZZA_HEN/runtime/payload_repository_source.json";
constexpr const char *kCatalog = "/data/PIZZA_HEN/runtime/payload_repository.json";
constexpr const char *kCatalogTmp = "/data/PIZZA_HEN/runtime/payload_repository.json.tmp";
constexpr const char *kPayloadDir = "/data/PIZZA_HEN/payloads";

struct RepoPayload {
  char name[128]{};
  char filename[256]{};
  char url[1024]{};
  char source[1024]{};
  char source_direct[1024]{};
  char description[1024]{};
  char last_update[64]{};
  char version[64]{};
  char checksum[65]{};
  char category[128]{};
};

static void ensure_dirs() {
  mkdir("/data/PIZZA_HEN",0777); mkdir("/data/PIZZA_HEN/runtime",0777); mkdir(kPayloadDir,0777);
}
static bool ends_with_ci(const std::string &s,const char *suffix) {
  const size_t n=strlen(suffix); if(s.size()<n)return false;
  for(size_t i=0;i<n;i++) if(std::tolower((unsigned char)s[s.size()-n+i])!=std::tolower((unsigned char)suffix[i])) return false;
  return true;
}
static std::string json_escape(const std::string &s) {
  std::string o; o.reserve(s.size()+8); static const char h[]="0123456789abcdef";
  for(unsigned char c:s){switch(c){case '\\':o+="\\\\";break;case '"':o+="\\\"";break;case '\n':o+="\\n";break;case '\r':o+="\\r";break;case '\t':o+="\\t";break;default:if(c<0x20){o+="\\u00";o+=h[(c>>4)&15];o+=h[c&15];}else o+=(char)c;}}
  return o;
}
// Payload Manager string extraction is retained; payload-array/object framing is tightened for the canonical PIZZA HEN catalog.
static int json_extract_string(const char *obj_start,const char *obj_end,const char *key,char *out,size_t out_size) {
  char key_pattern[96]; const char *p,*colon,*q; size_t pos=0;
  if(!out_size)return -1; out[0]='\0'; snprintf(key_pattern,sizeof(key_pattern),"\"%s\"",key);
  p=strstr(obj_start,key_pattern); if(!p||p>=obj_end)return -1;
  colon=strchr(p+strlen(key_pattern),':'); if(!colon||colon>=obj_end)return -1;
  q=colon+1; while(q<obj_end&&isspace((unsigned char)*q))q++;
  if(q>=obj_end||*q!='"')return -1; q++;
  while(q<obj_end&&*q!='"'){if(*q=='\\'&&(q+1)<obj_end)q++;if(pos+1<out_size)out[pos++]=*q;q++;}
  out[pos]='\0'; return 0;
}
static bool read_all(const char *path,std::string &out) {
  FILE *f=fopen(path,"rb"); if(!f)return false; if(fseek(f,0,SEEK_END)){fclose(f);return false;} long n=ftell(f); if(n<0||fseek(f,0,SEEK_SET)){fclose(f);return false;}
  out.resize((size_t)n); const size_t got=n?fread(out.data(),1,(size_t)n,f):0; fclose(f); if(got!=(size_t)n)return false; return true;
}
static bool valid_filename(const std::string &name) {
  if(name.empty()||name.size()>240||name.find('/')!=std::string::npos||name.find('\\')!=std::string::npos||name.find("..")!=std::string::npos)return false;
  return ends_with_ci(name,".elf");
}
static bool valid_sha256(const char *s) {
  if(!s || strlen(s)!=64)return false;
  for(size_t i=0;i<64;i++)if(!std::isxdigit((unsigned char)s[i]))return false;
  return true;
}
static bool parse_repo(const std::string &json,std::vector<RepoPayload> &items) {
  const char *all=json.c_str(), *end_all=all+json.size();
  const char *key=strstr(all,"\"payloads\"");
  const char *arr=nullptr;
  if(key){arr=strchr(key,'[');} else {arr=(const char*)memchr(all,'[',(size_t)(end_all-all));}
  if(!arr || arr>=end_all)return false;
  const char *p=arr+1;
  bool in_string=false, esc=false;
  int array_depth=1;
  const char *arr_end=end_all;
  for(const char *q=arr+1;q<end_all;q++){
    const char c=*q;
    if(in_string){if(esc){esc=false;continue;} if(c=='\\'){esc=true;continue;} if(c=='\"')in_string=false;continue;}
    if(c=='\"'){in_string=true;continue;}
    if(c=='[')array_depth++; else if(c==']' && --array_depth==0){arr_end=q;break;}
  }
  while(p<arr_end){
    while(p<arr_end && *p!='{')p++;
    if(p>=arr_end)break;
    const char *obj_start=p, *obj_end=nullptr;
    int depth=0; in_string=false; esc=false;
    for(const char *q=p;q<arr_end;q++){
      const char c=*q;
      if(in_string){if(esc){esc=false;continue;} if(c=='\\'){esc=true;continue;} if(c=='\"')in_string=false;continue;}
      if(c=='\"'){in_string=true;continue;}
      if(c=='{')depth++; else if(c=='}' && --depth==0){obj_end=q;break;}
    }
    if(!obj_end)break;
    RepoPayload item{};
    if(json_extract_string(obj_start,obj_end,"name",item.name,sizeof(item.name))==0 &&
       json_extract_string(obj_start,obj_end,"filename",item.filename,sizeof(item.filename))==0 &&
       json_extract_string(obj_start,obj_end,"url",item.url,sizeof(item.url))==0){
      json_extract_string(obj_start,obj_end,"source",item.source,sizeof(item.source));
      json_extract_string(obj_start,obj_end,"source_direct",item.source_direct,sizeof(item.source_direct));
      json_extract_string(obj_start,obj_end,"description",item.description,sizeof(item.description));
      json_extract_string(obj_start,obj_end,"last_update",item.last_update,sizeof(item.last_update));
      json_extract_string(obj_start,obj_end,"version",item.version,sizeof(item.version));
      json_extract_string(obj_start,obj_end,"checksum",item.checksum,sizeof(item.checksum));
      if(json_extract_string(obj_start,obj_end,"category",item.category,sizeof(item.category))!=0||!item.category[0])snprintf(item.category,sizeof(item.category),"Uncategorized");
      const std::string fn=item.filename;
      const bool url_ok=!strncmp(item.url,"https://",8)||!strncmp(item.url,"http://",7);
      if(valid_filename(fn)&&url_ok&&valid_sha256(item.checksum))items.push_back(item);
    }
    p=obj_end+1;
  }
  return !items.empty();
}
static bool write_source_cache(const std::string &raw) {
  const std::string tmp=std::string(kSourceCache)+".part";
  unlink(tmp.c_str());
  FILE *f=fopen(tmp.c_str(),"wb"); if(!f)return false;
  const size_t n=raw.size(); const size_t wrote=n?fwrite(raw.data(),1,n,f):0;
  if(wrote!=n){fclose(f);unlink(tmp.c_str());return false;}
  fflush(f); fsync(fileno(f)); fclose(f);
  if(rename(tmp.c_str(),kSourceCache)!=0){unlink(tmp.c_str());return false;}
  chmod(kSourceCache,0666); return true;
}
static bool valid_elf(const char *path) {
  int fd=open(path,O_RDONLY); if(fd<0)return false; unsigned char m[4]{}; const ssize_t n=read(fd,m,4); close(fd); return n==4&&m[0]==0x7f&&m[1]=='E'&&m[2]=='L'&&m[3]=='F';
}
static bool publish_catalog(const std::vector<RepoPayload> &items) {
  FILE *f=fopen(kCatalogTmp,"w"); if(!f)return false;
  fprintf(f,"{\n  \"schema\":\"pizzahen.payload-repository.v1\",\n  \"source\":\"%s\",\n  \"count\":%zu,\n  \"items\":[\n",kRepoSource,items.size());
  for(size_t i=0;i<items.size();i++){const auto &e=items[i];fprintf(f,"    {\"name\":\"%s\",\"filename\":\"%s\",\"url\":\"%s\",\"description\":\"%s\",\"version\":\"%s\",\"category\":\"%s\",\"checksum\":\"%s\"}%s\n",json_escape(e.name).c_str(),json_escape(e.filename).c_str(),json_escape(e.url).c_str(),json_escape(e.description).c_str(),json_escape(e.version).c_str(),json_escape(e.category).c_str(),json_escape(e.checksum).c_str(),i+1==items.size()?"":",");}
  fprintf(f,"  ]\n}\n");fflush(f);fsync(fileno(f));fclose(f);if(rename(kCatalogTmp,kCatalog)!=0){unlink(kCatalogTmp);return false;}chmod(kCatalog,0666);return true;
}
}

bool pizzahen_payload_repo_refresh() {
  ensure_dirs();
  const std::string raw(kPizzahenPayloadRepositoryJson);
  std::vector<RepoPayload> items; if(!parse_repo(raw,items))return false;
  if(!write_source_cache(raw))return false;
  return publish_catalog(items);
}

bool pizzahen_payload_repo_install(const std::string &filename) {
  ensure_dirs(); if(!valid_filename(filename))return false;
  std::string raw; if(!read_all(kSourceCache,raw)){if(!pizzahen_payload_repo_refresh()||!read_all(kSourceCache,raw))return false;}
  std::vector<RepoPayload> items; if(!parse_repo(raw,items))return false; const RepoPayload *pick=nullptr;
  for(const auto &e:items)if(filename==e.filename){pick=&e;break;} if(!pick)return false;
  const std::string part=std::string(kPayloadDir)+"/."+filename+".part"; const std::string dst=std::string(kPayloadDir)+"/"+filename; unlink(part.c_str());
  if(!download_file(pick->url,part.c_str())){unlink(part.c_str());return false;} if(!valid_elf(part.c_str())){unlink(part.c_str());return false;}
  if(strlen(pick->checksum)==64){char got[65]{};if(compute_sha256_file(part.c_str(),got)!=0||strcasecmp(got,pick->checksum)!=0){unlink(part.c_str());return false;}}
  if(rename(part.c_str(),dst.c_str())!=0){unlink(part.c_str());return false;}chmod(dst.c_str(),0777);(void)pizzahen_scan_plugin_catalog();return true;
}
