#include <iostream>
#include "include/count_min_sketch.hpp"

int main() {
    std::cout << "Running C++ Count-Min Sketch tests..." << std::endl;
    
    using namespace alltoolkit;
    
    CountMinSketch<int> sketch(5, 100);
    
    sketch.increment(1);
    sketch.increment(1);
    sketch.increment(2);
    
    std::cout << "hello estimate: " << sketch.estimate(1) << std::endl;
    std::cout << "world estimate: " << sketch.estimate(2) << std::endl;
    
    if (sketch.estimate(1) >= 2 && sketch.estimate(2) >= 1) {
        std::cout << "✓ Test 1: Basic increment PASSED" << std::endl;
    } else {
        std::cout << "✗ Test 1: FAILED" << std::endl;
    }
    
    CountMinSketch<int> sketch2(5, 100);
    sketch2.update(3, 5);
    
    if (sketch2.estimate(3) >= 5) {
        std::cout << "✓ Test 2: Update with delta PASSED" << std::endl;
    } else {
        std::cout << "✗ Test 2: FAILED" << std::endl;
    }
    
    std::cout << "total count: " << sketch.totalCount() << std::endl;
    
    std::cout << "✅ C++ tests completed!" << std::endl;
    return 0;
}
