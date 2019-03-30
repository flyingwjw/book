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
