CXX := clang++

CXXFLAGS := -O2 -fno-stack-protector -fno-pie -no-pie -s

TARGET := Avalanche

SRCS := $(wildcard src/*.cpp)

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRCS)

clean:
	rm -f $(TARGET)