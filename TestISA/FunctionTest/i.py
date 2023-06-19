cmds = """
$ cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D WITH_CUDA=ON -D CUDA_ARCH_BIN="6.2" -D CUDA_ARCH_PTX="" \
        -D WITH_CUBLAS=ON -D ENABLE_FAST_MATH=ON -D CUDA_FAST_MATH=ON \
        -D ENABLE_NEON=ON -D WITH_LIBV4L=ON -D BUILD_TESTS=OFF \
        -D BUILD_PERF_TESTS=OFF -D BUILD_EXAMPLES=OFF \
        -D WITH_GSTREAMER=ON -D WITH_GSTREAMER_0_10=OFF \
        -D WITH_QT=ON -D WITH_OPENGL=ON ..
$ make -j4
$ sudo make install
$ sudo ldconfig
"""
import os

cmd2  = []
for cmd in cmds.split('\n'):
    cmd2.append(cmd[2:]+'\n')

print(cmd2)

with open("commands.txt", "w+") as f:
    f.writelines(cmd2)

