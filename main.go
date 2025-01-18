package main

import (
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"sync"
)

var ax, ix, ay, iy, az, iz float64 = 0, 1e5, 0, 1e5, 0, 1e5
var item [][3]float64
var r0 float64
var count1, count2, totalCount int
var mutex sync.Mutex

const detectR = 1.1101

func refresh(c1, c2, c3 float64) {
	if ax < c1 {
		ax = c1
	}
	if ix > c1 {
		ix = c1
	}
	if ay < c2 {
		ay = c2
	}
	if iy > c2 {
		iy = c2
	}
	if az < c3 {
		az = c3
	}
	if iz > c3 {
		iz = c3
	}
}
func generateRandomFloat64(min, max float64) float64 {
	return min + rand.Float64()*(max-min)
}
func randomDot() [3]float64 {
	return [3]float64{generateRandomFloat64(ix, ax), generateRandomFloat64(iy, ay), generateRandomFloat64(iz, az)}
}
func initR0() {
	r0 = ax - ix
	if ay-iy < r0 {
		r0 = ay - iy
	}
	if az-iz < r0 {
		r0 = az - iz
	}
	r0 /= 2
}
func detectADot(p [3]float64) (bool, bool) {
	//bool1:严格法求体积 bool2:宽松法求体积
	var listOfCloseDot [][3]float64
	for _, i := range item {
		if (p[0]-i[0])*(p[0]-i[0])+(p[1]-i[1])*(p[1]-i[1])+(p[2]-i[2])*(p[2]-i[2]) <= detectR*detectR {
			listOfCloseDot = append(listOfCloseDot, i)
		}
	}
	if len(listOfCloseDot) == 0 {
		dx := (p[0]-(ax+ix)/2)*(p[0]-(ax+ix)/2) + (p[1]-(ay+iy)/2)*(p[1]-(ay+iy)/2) + (p[2]-(az+iz)/2)*(p[2]-(az+iz)/2)
		if dx <= r0*r0 {
			return true, true
		}
		return false, false
	} //此条处理了 （1）球内->true true（2）犄角旮旯->false false
	//下一条处理：球边缘处的情况
	return false, true
}
func detectADot1(p [3]float64) (bool, bool) {
	//bool1:严格法求体积 bool2:宽松法求体积
	for _, i := range item {
		if (p[0]-i[0])*(p[0]-i[0])+(p[1]-i[1])*(p[1]-i[1])+(p[2]-i[2])*(p[2]-i[2]) <= detectR*detectR {
			return false, true
		}
	}
	dx := (p[0]-(ax+ix)/2)*(p[0]-(ax+ix)/2) + (p[1]-(ay+iy)/2)*(p[1]-(ay+iy)/2) + (p[2]-(az+iz)/2)*(p[2]-(az+iz)/2)
	if dx <= r0*r0 {
		return true, true
	}
	return false, false
}
func worker(wg *sync.WaitGroup) {
	defer wg.Done()
	for {
		te := randomDot()
		b1, b2 := detectADot1(te)

		// 使用互斥锁确保并发访问共享变量时安全
		mutex.Lock()
		if b1 {
			count1++
		}
		if b2 {
			count2++
		}
		totalCount++
		if totalCount%1000000 == 0 {
			fmt.Println((ax - ix) * (ay - iy) * (az - iz) * float64(count1) / float64(totalCount))
			fmt.Println((ax-ix)*(ay-iy)*(az-iz)*float64(count2)/float64(totalCount), "total count:", totalCount)
			fmt.Println()
		}
		mutex.Unlock()
	}
}
func writeFile() {
	file, _ := os.Create("a.txt")
	defer file.Close()
	for totalCount < 100000000 {
		te := randomDot()
		b1, b2 := detectADot1(te)
		mutex.Lock()
		if !b1 && b2 {
			file.WriteString(fmt.Sprintf("%f", te[0]) + " " + fmt.Sprintf("%f", te[1]) + " " + fmt.Sprintf("%f", te[2]) + "\n")
		}
		totalCount++
		if totalCount%1000000 == 0 {
			fmt.Println("Total count:", totalCount)
		}
		mutex.Unlock()
	}
}

func main() {
	// 数据读取和初始化操作
	data, _ := os.ReadFile("140ns.xyz")
	fmt.Println(140)
	lines := strings.Split(string(data), "\n")
	for _, line := range lines {
		l := strings.Split(line, "  ")
		if len(l) == 3 {
			t1, _ := strconv.ParseFloat(l[0], 64)
			t2, _ := strconv.ParseFloat(l[1], 64)
			t3, _ := strconv.ParseFloat(strings.TrimSpace(l[2]), 64)
			item = append(item, [3]float64{t1, t2, t3})
			refresh(t1, t2, t3)
		}
	}
	initR0()
	//writeFile()
	var wg sync.WaitGroup
	for i := 1; i <= 8; i++ {
		wg.Add(1)
		go worker(&wg)
	}
	wg.Wait()
}