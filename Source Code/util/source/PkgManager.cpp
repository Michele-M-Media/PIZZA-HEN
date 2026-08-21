/*
 * PIZZA HEN Package catalogue.
 *
 * FIX70.20 keeps only PIZZA HEN's USB/EXT catalogue here.
 * Package installation is deliberately NOT performed by util/PkgManager.
 * The :8080 Toolbox launches the byte-exact websrv 0.34 PKGInstall payload
 * through websrv's own /hbldr endpoint, matching upstream's published model.
 */
#include <cctype>
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <strings.h>
#include <dirent.h>
#include <string>
#include <sys/stat.h>
#include <unistd.h>
#include <utility>
#include <vector>

namespace {
constexpr const char *kCatalog = "/data/PIZZA_HEN/runtime/pkg_catalog.json";
constexpr const char *kCatalogTmp = "/data/PIZZA_HEN/runtime/pkg_catalog.json.tmp";
constexpr int kMaxDepth = 4;
constexpr size_t kMaxPkgs = 512;

struct PackageEntry {
    std::string path;
    std::string name;
    std::string device;
    uint64_t size = 0;
    dev_t dev = 0;
    ino_t ino = 0;
};

std::vector<PackageEntry> g_packages;

static void ensure_runtime_dir() {
    mkdir("/data/PIZZA_HEN", 0777);
    mkdir("/data/PIZZA_HEN/runtime", 0777);
}

static std::string json_escape(const std::string &s) {
    std::string out; out.reserve(s.size()+8);
    static const char hex[]="0123456789abcdef";
    for (unsigned char c: s) {
        switch(c) {
        case '\\': out+="\\\\"; break; case '"': out+="\\\""; break;
        case '\n': out+="\\n"; break; case '\r': out+="\\r"; break; case '\t': out+="\\t"; break;
        default: if(c<0x20){ out+="\\u00"; out+=hex[(c>>4)&15]; out+=hex[c&15]; } else out+=(char)c;
        }
    }
    return out;
}

static bool ends_with_pkg(const char *name) {
    if(!name) return false;
    size_t n=strlen(name);
    if(n<4) return false;
    const char *e=name+n-4;
    return e[0]=='.' && std::tolower((unsigned char)e[1])=='p' &&
           std::tolower((unsigned char)e[2])=='k' && std::tolower((unsigned char)e[3])=='g';
}

static void scan_dir(const std::string &root,const std::string &device,int depth,std::vector<PackageEntry>&out) {
    if(depth>kMaxDepth||out.size()>=kMaxPkgs) return;
    DIR*d=opendir(root.c_str()); if(!d) return;
    while(dirent*ent=readdir(d)) {
        if(!strcmp(ent->d_name,".")||!strcmp(ent->d_name,"..")) continue;
        if(!strcasecmp(ent->d_name,"$RECYCLE.BIN")||!strcasecmp(ent->d_name,"System Volume Information")) continue;
        if(out.size()>=kMaxPkgs) break;
        std::string path=root; if(!path.empty()&&path.back()!='/') path+='/'; path+=ent->d_name;
        struct stat st{}; if(lstat(path.c_str(),&st)!=0) continue;
        if(S_ISDIR(st.st_mode)) scan_dir(path,device,depth+1,out);
        else if(S_ISREG(st.st_mode)&&ends_with_pkg(ent->d_name)) {
            bool dup=false; for(const auto&e:out) if(e.dev==st.st_dev&&e.ino==st.st_ino){dup=true;break;} if(dup) continue;
            out.push_back({path,ent->d_name,device,(uint64_t)st.st_size,st.st_dev,st.st_ino});
        }
    }
    closedir(d);
}

static int publish_catalog(const std::vector<PackageEntry>&list,const std::vector<std::string>&mounted) {
    ensure_runtime_dir(); FILE*f=fopen(kCatalogTmp,"w"); if(!f) return -1;
    fprintf(f,"{\n  \"schema\":\"pizzahen.pkg-catalog.v8-websrv034-upstream-pkginstall\",\n  \"roots\":[\"/mnt/usb0..7\",\"/mnt/ext0\",\"/mnt/ext1\",\"/usb0..7\"],\n  \"mounted_roots\":[");
    for(size_t i=0;i<mounted.size();++i) fprintf(f,"\"%s\"%s",json_escape(mounted[i]).c_str(),i+1==mounted.size()?"":",");
    fprintf(f,"],\n  \"count\":%zu,\n  \"packages\":[\n",list.size());
    for(size_t i=0;i<list.size();++i){const auto&e=list[i];fprintf(f,"    {\"index\":%zu,\"name\":\"%s\",\"path\":\"%s\",\"device\":\"%s\",\"size\":%llu}%s\n",i,json_escape(e.name).c_str(),json_escape(e.path).c_str(),json_escape(e.device).c_str(),(unsigned long long)e.size,i+1==list.size()?"":",");}
    fprintf(f,"  ]\n}\n"); fflush(f); fsync(fileno(f)); fclose(f);
    if(rename(kCatalogTmp,kCatalog)!=0){unlink(kCatalogTmp);return -2;} chmod(kCatalog,0666); return 0;
}
} // namespace

int pizzahen_pkg_scan_usb(void){
    std::vector<PackageEntry>found; std::vector<std::string>mounted; struct RootSpec{std::string path,label;}; std::vector<RootSpec>roots;
    for(int i=0;i<=7;++i){char p[32],l[16];snprintf(p,sizeof(p),"/mnt/usb%d",i);snprintf(l,sizeof(l),"USB%d",i);roots.push_back({p,l});}
    roots.push_back({"/mnt/ext0","EXT0"}); roots.push_back({"/mnt/ext1","EXT1"});
    for(int i=0;i<=7;++i){char p[16],l[20];snprintf(p,sizeof(p),"/usb%d",i);snprintf(l,sizeof(l),"USB%d-ALIAS",i);roots.push_back({p,l});}
    std::vector<std::pair<dev_t,ino_t>>seen;
    for(const auto&spec:roots){if(found.size()>=kMaxPkgs)break;struct stat st{};if(stat(spec.path.c_str(),&st)!=0||!S_ISDIR(st.st_mode))continue;mounted.push_back(spec.path);bool same=false;for(const auto&id:seen)if(id.first==st.st_dev&&id.second==st.st_ino){same=true;break;}if(same)continue;seen.push_back({st.st_dev,st.st_ino});scan_dir(spec.path,spec.label,0,found);}
    g_packages.swap(found);int count=(int)g_packages.size();int rc=publish_catalog(g_packages,mounted);return rc==0?count:rc;
}
