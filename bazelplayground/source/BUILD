cc_library(
    name="hello-time",
    srcs=["hello-time.cpp"],
    hdrs=["hello-time.h"],
    )

cc_binary(
    name="hello-world",
    srcs=["hello-world.cpp"],
    deps=[
        ":hello-time",
        "//lib:hello-greet"
    ],
    )
