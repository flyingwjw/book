# GitBook

## 环境搭建

```
$ npm install gitbook-cli -g
```

## 常用命令

```
$ gitbook help

build [book] [output]           build a book
        --log                   Minimum log level to display (Default is info; Values are debug, info, warn, error, disabled)
        --format                Format to build to (Default is website; Values are website, json, ebook)
        --[no-]timing           Print timing debug information (Default is false)

    serve [book] [output]       serve the book as a website for testing
        --port                  Port for server to listen on (Default is 4000)
        --lrport                Port for livereload server to listen on (Default is 35729)
        --[no-]watch            Enable file watcher and live reloading (Default is true)
        --[no-]live             Enable live reloading (Default is true)
        --[no-]open             Enable opening book in browser (Default is false)
        --browser               Specify browser for opening book (Default is )
        --log                   Minimum log level to display (Default is info; Values are debug, info, warn, error, disabled)
        --format                Format to build to (Default is website; Values are website, json, ebook)

    install [book]              install all plugins dependencies
        --log                   Minimum log level to display (Default is info; Values are debug, info, warn, error, disabled)

    parse [book]                parse and print debug information about a book
        --log                   Minimum log level to display (Default is info; Values are debug, info, warn, error, disabled)

    init [book]                 setup and create files for chapters
        --log                   Minimum log level to display (Default is info; Values are debug, info, warn, error, disabled)

    pdf [book] [output]         build a book into an ebook file
        --log                   Minimum log level to display (Default is info; Values are debug, info, warn, error, disabled)

    epub [book] [output]        build a book into an ebook file
        --log                   Minimum log level to display (Default is info; Values are debug, info, warn, error, disabled)

    mobi [book] [output]        build a book into an ebook file
        --log                   Minimum log level to display (Default is info; Values are debug, info, warn, error, disabled)
```
### 构建
#### 构建html
```
$ gitbook build test
```

#### 构建PDF
```
$ gitbook pdf test
```

1. 出现错误“ebook-convert" is not installed

```
    kevin@kevin:/mnt/shared_hd/book$ gitbook  pdf test
    info: 7 plugins are installed 
    info: 6 explicitly listed 
    info: loading plugin "highlight"... OK 
    info: loading plugin "search"... OK 
    info: loading plugin "lunr"... OK 
    info: loading plugin "sharing"... OK 
    info: loading plugin "fontsettings"... OK 
    info: loading plugin "theme-default"... OK 
    info: found 16 pages 
    info: found 0 asset files 

    InstallRequiredError: "ebook-convert" is not installed.
    Install it from Calibre: https://calibre-ebook.com
```
* ebook-convert不是内部或外部命令，原因是GitBook在生成PDF的过程中使用到calibre的转换功能，没有安装calibre或安装了calibre没有配置环境变量都会导致转换PDF失败

2. 安装calibre出错
```
$ sudo -v && wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sudo sh /dev/stdin
ERROR: cannot verify download.calibre-ebook.com's certificate, issued by ‘CN=Let's Encrypt Authority X3,O=Let's Encrypt,C=US’:
  Unable to locally verify the issuer's authority.
To connect to download.calibre-ebook.com insecurely, use `--no-check-certificate'.
```

解决方法：
```
$ wget --no-check-certificate https://github.com/curl/curl/raw/master/lib/mk-ca-bundle.pl
$ perl mk-ca-bundle.pl && rm certdata.txt
$ mkdir -p ~/.ssl/ && mv ca-bundle.crt mk-ca-bundle.pl ~/.ssl
$ echo "ca_certificate = ~/.ssl/ca-bundle.crt" >> ~/.wgetrc
```
将他设置到CURL的环境变量 CURL_CA_BUNDLE 即:
export CURL_CA_BUNDLE = ~/.ssl/ca-bundle.crt
(编辑文件 ~/.profile, ~/.bash_profile 等文件，增加以上行让他永久生效)

* 安装calibre最好世界使用官网编译好的二进制包，自己搭环境问题太多。
* 使用calibre生成的pdf很大，不知道是不是配置问题。

### Deploy

```
$ ./deploy.sh
```

或者

```
$ gitbook init test
$ gitbook build test share/test
$ cp -rf share ../flyingwjw.github.io
```
注意：flyingwjw.github.io目录位置要根据实际情况修改，该目录是仓库 https://github.com/flyingwjw/flyingwjw.github.io.git的本地目录。

编译本地test目录输出到share/test目录，把share目录放到github仓库 https://github.com/flyingwjw/flyingwjw.github.io.git 中, 这样就可以直接访问https://flyingwjw.github.io/share/test 来访问test book的内容。直接访问 https://flyingwjw.github.io 还是Hexo生成的网页，与gitbook生成的网页没有冲突，扩展了github免费web服务器的使用，哈哈。
