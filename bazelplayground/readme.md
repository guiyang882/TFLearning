## bazelplayground
主要是用来学习bazel组织和管理工程相关的操作

### build first cpp proj  
```bash
.
├── BUILD.old
├── lib
│   ├── BUILD
│   ├── hello-greet.cpp
│   └── hello-greet.h
├── readme.md
├── source
│   ├── BUILD
│   ├── hello-time.cpp
│   ├── hello-time.h
│   └── hello-world.cpp
└── WORKSPACE

bazel build source:hello-world
```


### Transitive includes  
If a file includes a header, then the file's rule should depend on that header's library. Conversely, only direct dependencies need to be specified as dependencies. For example, suppose sandwich.h includes bread.h and bread.h includes flour.h. sandwich.h doesn't include flour.h (who wants flour in their sandwich?), so the BUILD file would look like:

```
cc_library(
    name = "sandwich",
    srcs = ["sandwich.cc"],
    hdrs = ["sandwich.h"],
    deps = [":bread"],
)

cc_library(
    name = "bread",
    srcs = ["bread.cc"],
    hdrs = ["bread.h"],
    deps = [":flour"],
)

cc_library(
    name = "flour",
    srcs = ["flour.cc"],
    hdrs = ["flour.h"],
)

```
