/*
 * FIX70.24 - PIZZA HEN Plugins / Payload ELFs catalogue.
 *
 * Functional model is grounded in etaHEN generate_plugin_xml(): scan the
 * plugins and payloads directories, validate .plugin CustomPluginHeader,
 * expose Start/Stop state and use <path>.auto_start marker files.  The owned
 * web Toolbox consumes JSON instead of legacy ShellUI XML.
 */
#include <plugin_manager.hpp>
extern "C" {
#include "common_utils.h"
}
#include <algorithm>
#include <cerrno>
#include <cstdlib>
#include <cstdint>
#include <cctype>
#include <cstdio>
#include <cstring>
#include <dirent.h>
#include <fcntl.h>
#include <signal.h>
#include <string>
#include <sys/stat.h>
#include <unistd.h>
#include <vector>

extern "C" int sceKernelGetProcessName(int pid, char *name);

namespace {
constexpr const char *kCatalog = "/data/PIZZA_HEN/runtime/plugin_catalog.json";
constexpr const char *kCatalogTmp = "/data/PIZZA_HEN/runtime/plugin_catalog.json.tmp";
constexpr const char *kCatalogUser = "/user/data/PIZZA_HEN/runtime/plugin_catalog.json";
constexpr const char *kCatalogUserTmp = "/user/data/PIZZA_HEN/runtime/plugin_catalog.json.tmp";

struct Entry {
  std::string path, name, kind, title_id, version, root;
  int pid = -1;
  bool running = false;
  bool auto_start = false;
};

static bool ends_with_ci(const std::string &s, const char *suffix) {
  const size_t n = strlen(suffix);
  if (s.size() < n) return false;
  for (size_t i=0;i<n;i++)
    if (std::tolower((unsigned char)s[s.size()-n+i]) != std::tolower((unsigned char)suffix[i])) return false;
  return true;
}
static std::string json_escape(const std::string &s) {
  std::string o; o.reserve(s.size()+8); static const char h[]="0123456789abcdef";
  for (unsigned char c: s) { switch(c) {
    case '\\': o+="\\\\"; break; case '"': o+="\\\""; break;
    case '\n': o+="\\n"; break; case '\r': o+="\\r"; break; case '\t': o+="\\t"; break;
    default: if(c<0x20){o+="\\u00";o+=h[(c>>4)&15];o+=h[c&15];}else o+=(char)c;
  }} return o;
}
static bool file_exists(const std::string &p) { struct stat st{}; return stat(p.c_str(), &st)==0; }
static int read_pid(const std::string &p) {
  int fd=open(p.c_str(),O_RDONLY); if(fd<0)return -1; char b[32]{}; int n=read(fd,b,sizeof(b)-1); close(fd); return n>0?atoi(b):-1;
}
static bool pid_alive(int pid) {
  if(pid<=0)return false; char name[64]{}; return sceKernelGetProcessName(pid,name)>=0;
}
static bool valid_plugin_header(const CustomPluginHeader &h) {
  return memcmp(h.prefix,"etaHEN_PLUGIN",13)==0 && h.titleID[0] != 0;
}
static bool valid_elf_magic(int fd) {
  unsigned char m[4]{}; if(lseek(fd,0,SEEK_SET)<0)return false; return read(fd,m,4)==4 && m[0]==0x7f&&m[1]=='E'&&m[2]=='L'&&m[3]=='F';
}
static void add_dir(const std::string &root, std::vector<Entry> &out) {
  DIR *d=opendir(root.c_str()); if(!d)return;
  while(dirent *de=readdir(d)) {
    if(!strcmp(de->d_name,".")||!strcmp(de->d_name,".."))continue;
    std::string name=de->d_name;
    if(ends_with_ci(name,".auto_start"))continue;
    const bool is_plugin=ends_with_ci(name,".plugin"), is_elf=ends_with_ci(name,".elf");
    if(!is_plugin&&!is_elf)continue;
    std::string path=root+"/"+name;
    int fd=open(path.c_str(),O_RDONLY); if(fd<0)continue;
    Entry e; e.path=path; e.name=name; e.root=root; e.kind=is_plugin?"plugin":"payload";
    std::string pidpath;
    if(is_plugin) {
      CustomPluginHeader h{}; if(read(fd,&h,sizeof(h))!=(ssize_t)sizeof(h)||!valid_plugin_header(h)){close(fd);continue;}
      h.titleID[sizeof(h.titleID)-1]=0; h.plugin_version[sizeof(h.plugin_version)-1]=0;
      e.title_id=h.titleID; e.version=h.plugin_version;
      pidpath="/system_tmp/"+e.title_id+".PID";
    } else {
      if(!valid_elf_magic(fd)){close(fd);continue;}
      char pbuf[256]; pizzahen_payload_pid_path(path.c_str(),pbuf,sizeof(pbuf)); pidpath=pbuf;
      e.title_id=name;
    }
    close(fd);
    e.pid=read_pid(pidpath); e.running=pid_alive(e.pid);
    if(e.pid>0&&!e.running) { unlink(pidpath.c_str()); e.pid=-1; }
    e.auto_start=file_exists(path+".auto_start");
    out.push_back(e);
  }
  closedir(d);
}
static void ensure_dirs() {
  mkdir("/data/PIZZA_HEN",0777); mkdir("/data/PIZZA_HEN/runtime",0777);
  mkdir("/data/PIZZA_HEN/plugins",0777); mkdir("/data/PIZZA_HEN/payloads",0777);
  mkdir("/user/data/PIZZA_HEN",0777); mkdir("/user/data/PIZZA_HEN/runtime",0777);
}
static bool write_catalog(const char *tmp, const char *dst, const std::vector<Entry> &unique) {
  FILE *f=fopen(tmp,"w"); if(!f)return false;
  fprintf(f,"{\n  \"schema\":\"pizzahen.plugin-catalog.v1\",\n  \"count\":%zu,\n  \"items\":[\n",unique.size());
  for(size_t i=0;i<unique.size();i++) { const auto&e=unique[i];
    fprintf(f,"    {\"index\":%zu,\"kind\":\"%s\",\"name\":\"%s\",\"path\":\"%s\",\"title_id\":\"%s\",\"version\":\"%s\",\"running\":%s,\"pid\":%d,\"auto_start\":%s}%s\n",
      i,e.kind.c_str(),json_escape(e.name).c_str(),json_escape(e.path).c_str(),json_escape(e.title_id).c_str(),json_escape(e.version).c_str(),e.running?"true":"false",e.pid,e.auto_start?"true":"false",i+1==unique.size()?"":",");
  }
  fprintf(f,"  ]\n}\n"); fflush(f); fsync(fileno(f)); fclose(f);
  if(rename(tmp,dst)!=0){unlink(tmp);return false;} chmod(dst,0666); return true;
}
}

bool pizzahen_scan_plugin_catalog() {
  ensure_dirs(); std::vector<Entry> v;
  add_dir("/data/PIZZA_HEN/plugins",v); add_dir("/data/PIZZA_HEN/payloads",v);
  // Existing PIZZA user-data alias plus the exact legacy etaHEN roots used by
  // generate_plugin_xml()/hardware logs. These are scanned only when present.
  add_dir("/user/data/PIZZA_HEN/plugins",v); add_dir("/user/data/PIZZA_HEN/payloads",v);
  add_dir("/data/etaHEN/plugins",v); add_dir("/data/etaHEN/payloads",v);
  add_dir("/user/data/etaHEN/plugins",v); add_dir("/user/data/etaHEN/payloads",v);
  for(int i=0;i<8;i++) {
    char root[160];
    snprintf(root,sizeof(root),"/mnt/usb%d/PIZZA_HEN/plugins",i); add_dir(root,v);
    snprintf(root,sizeof(root),"/mnt/usb%d/PIZZA_HEN/payloads",i); add_dir(root,v);
    snprintf(root,sizeof(root),"/usb%d/PIZZA_HEN/plugins",i); add_dir(root,v);
    snprintf(root,sizeof(root),"/usb%d/PIZZA_HEN/payloads",i); add_dir(root,v);
    snprintf(root,sizeof(root),"/mnt/usb%d/etaHEN/plugins",i); add_dir(root,v);
    snprintf(root,sizeof(root),"/mnt/usb%d/etaHEN/payloads",i); add_dir(root,v);
    snprintf(root,sizeof(root),"/usb%d/etaHEN/plugins",i); add_dir(root,v);
    snprintf(root,sizeof(root),"/usb%d/etaHEN/payloads",i); add_dir(root,v);
    if(i<4){
      snprintf(root,sizeof(root),"/mnt/ext%d/PIZZA_HEN/plugins",i); add_dir(root,v);
      snprintf(root,sizeof(root),"/mnt/ext%d/PIZZA_HEN/payloads",i); add_dir(root,v);
      snprintf(root,sizeof(root),"/mnt/ext%d/etaHEN/plugins",i); add_dir(root,v);
      snprintf(root,sizeof(root),"/mnt/ext%d/etaHEN/payloads",i); add_dir(root,v);
    }
  }
  // Deduplicate aliases by absolute path suffix/name/title pair while preferring /mnt.
  std::vector<Entry> unique;
  for(const auto &e:v) {
    bool dup=false; for(const auto &u:unique) if(e.name==u.name&&e.title_id==u.title_id&&e.kind==u.kind&&e.path!=u.path&&
      (((e.path.rfind("/usb",0)==0&&u.path.rfind("/mnt/usb",0)==0)||(u.path.rfind("/usb",0)==0&&e.path.rfind("/mnt/usb",0)==0)) ||
       ((e.path.rfind("/user/data/PIZZA_HEN/",0)==0&&u.path.rfind("/data/PIZZA_HEN/",0)==0)||(u.path.rfind("/user/data/PIZZA_HEN/",0)==0&&e.path.rfind("/data/PIZZA_HEN/",0)==0)))){dup=true;break;}
    if(!dup)unique.push_back(e);
  }
  const bool canonical_ok=write_catalog(kCatalogTmp,kCatalog,unique);
  const bool user_ok=write_catalog(kCatalogUserTmp,kCatalogUser,unique);
  return canonical_ok || user_ok;
}

bool pizzahen_stop_plugin(const std::string &path, const std::string &title_id, bool is_payload) {
  char pbuf[256]{};
  if(is_payload) pizzahen_payload_pid_path(path.c_str(),pbuf,sizeof(pbuf));
  else snprintf(pbuf,sizeof(pbuf),"/system_tmp/%s.PID",title_id.c_str());
  int pid=read_pid(pbuf); if(pid<=0){unlink(pbuf);return true;}
  if(pid_alive(pid) && kill(pid,SIGKILL)!=0)return false;
  unlink(pbuf); return true;
}

bool pizzahen_set_plugin_autostart(const std::string &path, bool enabled) {
  if(path.empty() || path.find('"')!=std::string::npos || path.find("..")!=std::string::npos) return false;
  // Only files under PIZZA HEN-owned data/USB plugin or payload roots.
  const bool owned = path.rfind("/data/PIZZA_HEN/",0)==0 || path.rfind("/user/data/PIZZA_HEN/",0)==0 ||
                     path.rfind("/data/etaHEN/",0)==0 || path.rfind("/user/data/etaHEN/",0)==0 ||
                     path.rfind("/mnt/usb",0)==0 || path.rfind("/usb",0)==0 || path.rfind("/mnt/ext",0)==0;
  if(!owned || (!ends_with_ci(path,".plugin")&&!ends_with_ci(path,".elf")))return false;
  const std::string marker=path+".auto_start";
  if(!enabled){ if(unlink(marker.c_str())!=0&&errno!=ENOENT)return false; return true; }
  int fd=open(marker.c_str(),O_WRONLY|O_CREAT|O_TRUNC,0666); if(fd<0)return false; close(fd); return true;
}


bool pizzahen_stop_all_managed_plugins() {
  ensure_dirs();
  std::vector<Entry> v;
  add_dir("/data/PIZZA_HEN/plugins",v); add_dir("/data/PIZZA_HEN/payloads",v);
  add_dir("/user/data/PIZZA_HEN/plugins",v); add_dir("/user/data/PIZZA_HEN/payloads",v);
  for(int i=0;i<8;i++) {
    char root[160];
    snprintf(root,sizeof(root),"/mnt/usb%d/PIZZA_HEN/plugins",i); add_dir(root,v);
    snprintf(root,sizeof(root),"/mnt/usb%d/PIZZA_HEN/payloads",i); add_dir(root,v);
    snprintf(root,sizeof(root),"/usb%d/PIZZA_HEN/plugins",i); add_dir(root,v);
    snprintf(root,sizeof(root),"/usb%d/PIZZA_HEN/payloads",i); add_dir(root,v);
    snprintf(root,sizeof(root),"/mnt/usb%d/etaHEN/plugins",i); add_dir(root,v);
    snprintf(root,sizeof(root),"/mnt/usb%d/etaHEN/payloads",i); add_dir(root,v);
    snprintf(root,sizeof(root),"/usb%d/etaHEN/plugins",i); add_dir(root,v);
    snprintf(root,sizeof(root),"/usb%d/etaHEN/payloads",i); add_dir(root,v);
    if(i<4){
      snprintf(root,sizeof(root),"/mnt/ext%d/PIZZA_HEN/plugins",i); add_dir(root,v);
      snprintf(root,sizeof(root),"/mnt/ext%d/PIZZA_HEN/payloads",i); add_dir(root,v);
      snprintf(root,sizeof(root),"/mnt/ext%d/etaHEN/plugins",i); add_dir(root,v);
      snprintf(root,sizeof(root),"/mnt/ext%d/etaHEN/payloads",i); add_dir(root,v);
    }
  }
  bool ok=true;
  std::vector<int> seen;
  for(const auto &e:v) {
    if(e.pid<=0 || !e.running) continue;
    if(std::find(seen.begin(),seen.end(),e.pid)!=seen.end()) continue;
    seen.push_back(e.pid);
    if(kill(e.pid,SIGKILL)!=0 && errno!=ESRCH) ok=false;
    char pbuf[256]{};
    if(e.kind=="payload") pizzahen_payload_pid_path(e.path.c_str(),pbuf,sizeof(pbuf));
    else snprintf(pbuf,sizeof(pbuf),"/system_tmp/%s.PID",e.title_id.c_str());
    unlink(pbuf);
  }
  (void)pizzahen_scan_plugin_catalog();
  return ok;
}
