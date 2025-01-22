# 利用Github workflow运算投掷点
## Github workflow的特性
1.免费  
2.对于公共仓库，每个job可以运行6小时  
3.可以同时运行20个workflow  
4.实时输出  
5.可以自选操作系统，可以读取文件

## 使用Github workflow进行此运算的步骤
1.批量上传数据文件，即xxns.xyz  
2.配置yaml文件，在main分支受更改时启动workflow  
```yaml
name: Go

on:
  push:
    branches: [ "main" ]

jobs:

  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Go
      uses: actions/setup-go@v4
      with:
        go-version: '1.20'

    - name: Build
      run: go build -v main.go

    - name: Run
      run: ./main
```
3.利用Github令牌，设置Python程序更改main分支中main.go代码文件，这就会启动Github workflow
```python
import time
import requests
import base64

username = 'jiananlan' 
repo = 'test' 
file_path = 'main.go' 
branch = 'main' 
token = '请更改为您的Github令牌'
api_url = f'https://api.github.com/repos/{username}/{repo}/contents/{file_path}?ref={branch}'


def update_file_content(new_content):
    headers = {'Authorization': f'token {token}'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        file_info = response.json()
        sha = file_info['sha'] # 获取sha值，其标识当前版本

        new_content_base64 = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')
        update_url = f'https://api.github.com/repos/{username}/{repo}/contents/{file_path}'
        data = {
            'message': 'Update main.go', 
            'content': new_content_base64,  # 新的文件内容（Base64编码）
            'sha': sha,  
            'branch': branch  
        }

        response = requests.put(update_url, headers=headers, json=data)

        if response.status_code == 200:
            print("成功")
        else:
            print(f"失败{response.status_code}")


if __name__ == "__main__":
    with open("code.txt", "r", encoding='utf-8') as f:
        content = f.read() # code.txt文件为go代码文件，涉及读取哪一组数据的部分使用了一个字符串代替，replace为相应组的数据即可
    for i in range(46):
        print('正在启动', i*10, 'ns数据的运算',sep='', end='--->')
        update_file_content(content.replace("****%%%%$$$****",str(i*10)),)
        time.sleep(8)
```
4.运用编译后的程序计算6小时的随机投掷点，输出所求体积（可以进行4.1亿以上次的运算）   
5.使用go代码，运用go语言遍历速度快，并行效率高的优点
```go
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

func main() {
	data, _ := os.ReadFile("****%%%%$$$****ns.xyz")
	fmt.Println(****%%%%$$$****)
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
	var wg sync.WaitGroup
	for i := 1; i <= 8; i++ {
		wg.Add(1)
		go worker(&wg)
	}
	wg.Wait()
}
```
6.收集输出数据  
