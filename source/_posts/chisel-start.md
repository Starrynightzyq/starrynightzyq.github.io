---
title: chisel 学习（1）
toc: true
comments: true
date: 2021-05-24 19:29:18
updated: 2022-03-29 11:28:33
categories: chisel
tags: [chisel, FPGA]
description: 
---

![Chisel 3](https://pic.zhouyuqian.com/img/20210726235317.svg)

<!--more-->

# 什么是 chisel

https://www.chisel-lang.org/

# 学习资料

1. [Chisel Bootcamp](https://github.com/freechipsproject/chisel-bootcamp)是一个很不错的chisel教程, 还支持在线运行chisel代码, 你可以一边编写chisel代码一边学习. 其中
   - 第1章是scala入门
   - 第2章是chisel基础
   - 第3章是scala高级特性和chisel的混合使用
   - 第4章是FIRRTL后端相关内容 你需要完成前两章的学习, 同时我们强烈建议你学习第3章. 第4章和本课程没有直接关系, 可以作为课外阅读材料.
2. [Chisel Bootcamp 中文](https://www.chiselchina.com/archives/) 这个是翻译成中文的 Chisel Bootcamp
3. [Chisel Users Guideopen in new window](https://www.chisel-lang.org/chisel3/docs/introduction.html)比较系统地整理了chisel的特性, 也是不错的入门教程.
4. [Chisel API](https://www.chisel-lang.org/api/latest/chisel3/index.html)详细地列出了chisel库的所有API供参考.
5. [Chisel小抄open in new window](https://github.com/freechipsproject/chisel-cheatsheet/releases/latest/download/chisel_cheatsheet.pdf)简明地列出了chisel语言的大部分用法.
6. [schoeberl/chisel-book](https://github.com/schoeberl/chisel-book)
7. [schoeberl/chisel-examples](https://github.com/schoeberl/chisel-examples)

# 安装

[Installing sbt](https://www.scala-sbt.org/release/docs/Setup.html#Installing+sbt)

Follow the instructions from [Chisel3](https://github.com/freechipsproject/chisel3) and [firrtl](https://github.com/freechipsproject/firrtl) websites.



Docker:

~~~
https://github.com/muojp/docker-sbt-chisel.git
~~~

OR: 使用 [OpenXiangShan/chisel-playground](https://github.com/OpenXiangShan/chisel-playground.git) 项目，已经配置好了环境，使用 [mill](https://com-lihaoyi.github.io/mill) 作为 Scala 编译器.


# Before Start

首先需要理解Scala：



# 语法

## Variables and Constants - var and val

推荐使用 val (常量)

## Seq

## when

**等于**要使用 `===`

~~~scala
when ( myData === 3.U ) {
  // Some logic to run when myData equals 3.
} .elsewhen ( myData === 1.U ) {
   // Some logic to run when myData equals 1.
} .otherwise {
  // Some logic to run when myData is neither 3 nor 1.
}
~~~

~~~scala
  // Returns the current `when` condition
when (a) {
  when (b) {
    when (c) {
    }.otherwise {
      when.cond // this is equal to: a && b && !c
    }
  }
}
~~~

## for

其功能相当于 Verilog 中的 generator

~~~scala
for(i <- 0 until consts.length) {
      muls += regs(i) * consts(i).U
} 
~~~

## if or when ?

`if` 是 scala 的语法，不能综合；

`when` 是 chisel 的语法，等同于 Verilog 中的 `if`；

~~~scala
class RegisterFile(readPorts: Int) extends Module {
    require(readPorts >= 0)
    val io = IO(new Bundle {
        val wen   = Input(Bool())
        val waddr = Input(UInt(5.W))
        val wdata = Input(UInt(32.W))
        val raddr = Input(Vec(readPorts, UInt(5.W)))
        val rdata = Output(Vec(readPorts, UInt(32.W)))
    })
    
    // A Register of a vector of UInts
    val reg = RegInit(VecInit(Seq.fill(32)(0.U(32.W))))
    
    when(io.wen) {
        reg(io.waddr) := io.wdata
    }
    
    for(i <- 0 until readPorts) {
        when(io.raddr(i) === 0.U) {
            io.rdata(i) := 0.U(32.W)
        }.otherwise {
            io.rdata(i) := reg(io.raddr(i))
        }
//         if(io.raddr(i) == 0.U) io.rdata(i) := 0.U(32.W)
//         else io.rdata(i) := reg(io.raddr(i))
    }
}
~~~

## 加法

```scala
// a +& b 包含进位, 而 a + b 不包含
io.sum := io.in0 +& io.in1
```

## 获得 Verilog 代码

~~~scala
println(getVerilog(new <module>))
~~~

## 可视化

~~~scala
visualize(() => new <module>)
~~~

## 带有`Decoupled`接口的模块

`Decoupled`可以将基本的chisel数据类型包装起来，并为其提供`ready`和`valid`信号。 Testers2提供了一些很好的工具，可以自动并可靠地测试这些接口。

~~~scala
case class QueueModule[T <: Data](ioType: T, entries: Int) extends MultiIOModule {
  val in = IO(Flipped(Decoupled(ioType)))
  val out = IO(Decoupled(ioType))
  out <> Queue(in, entries)
}
visualize(() => new QueueModule(UInt(9.W), entries = 200))
println(getVerilog(new QueueModule(UInt(9.W), entries = 200)))
~~~

![q](https://pic.zhouyuqian.com/img/20210727174715.png)

**计算最大公约数：**

**src**

~~~scala
// 输入接口
class GcdInputBundle(val w: Int) extends Bundle {
  val value1 = UInt(w.W)
  val value2 = UInt(w.W)
}
// 输出接口
class GcdOutputBundle(val w: Int) extends Bundle {
  val value1 = UInt(w.W)
  val value2 = UInt(w.W)
  val gcd    = UInt(w.W)
}
// GCD
/**
  * 使用减法来计算GCD。
  * 从寄存器 x 和 y 中较大一个中减去较小的一个，直到寄存器 y 为零。
  * 输入寄存器 x 的值就是最大公约数
  * 返回包含两个输入值及其GCD的包
  */

class DecoupledGcd(width: Int) extends MultiIOModule {

  val input = IO(Flipped(Decoupled(new GcdInputBundle(width))))
  val output = IO(Decoupled(new GcdOutputBundle(width)))

  val xInitial    = Reg(UInt())
  val yInitial    = Reg(UInt())
  val x           = Reg(UInt())
  val y           = Reg(UInt())
  val busy        = RegInit(false.B)
  val resultValid = RegInit(false.B)

  input.ready := ! busy
  output.valid := resultValid
  output.bits := DontCare

  when(busy)  {
    // 在计算期间，从每次较大的值中减去较小的值
    when(x > y) {
      x := x - y
    }.otherwise {
      y := y - x
    }
    when(y === 0.U) {
      // 当 y 变为零时，计算结束，将输出置为 valid
      output.bits.gcd := x
      output.bits.value1 := xInitial
      output.bits.value2 := yInitial
      output.bits.gcd := x
      output.valid := true.B
      busy := false.B
    }
  }.otherwise {
    when(input.valid) {
      // 当有可用的有效数据且没有进行计算时，获取新值并开始计算
      val bundle = input.deq()
      x := bundle.value1
      y := bundle.value2
      xInitial := bundle.value1
      yInitial := bundle.value2
      busy := true.B
      resultValid := false.B
    }
  }
}
~~~

**tb**

~~~scala
test(new DecoupledGcd(16)) { dut =>
  dut.input.initSource().setSourceClock(dut.clock)
  dut.output.initSink().setSinkClock(dut.clock)

  val testValues = for { x <- 1 to 10; y <- 1 to 10} yield (x, y)
  val inputSeq = testValues.map { case (x, y) =>
    (new GcdInputBundle(16)).Lit(_.value1 -> x.U, _.value2 -> y.U)
  }
  val resultSeq = testValues.map { case (x, y) =>
    new GcdOutputBundle(16).Lit(_.value1 -> x.U, _.value2 -> y.U, _.gcd -> BigInt(x).gcd(BigInt(y)).U)
  }

  // fork join 并行测试
  fork {
    dut.input.enqueueSeq(inputSeq)
  }.fork {
    dut.output.expectDequeueSeq(resultSeq)
  }.join()
}
~~~

## Queues

`Queue` creates a FIFO (first-in, first-out) queue with Decoupled interfaces on both sides, allowing backpressure. Both the data type and number of elements are configurable.

~~~scala
class MyQueue(width: Int, len: Int) extends Module {
    val io = IO(new Bundle {
        val in = Flipped(Decoupled(UInt(width.W)))
        val out = Decoupled(UInt(width.W))
    })
    val fifo = Queue(io.in, len)
    io.out <> fifo
}

visualize(() => new MyQueue(32, 10))
println(getVerilog(new MyQueue(32, 10)))
~~~

![Queues](https://pic.zhouyuqian.com/img/20210727174733.png)

## Arbiters

Arbiters routes data from *n* `DecoupledIO` sources to one `DecoupledIO` sink, given a prioritization. There are two types included in Chisel:

- `Arbiter`: prioritizes lower-index producers
- `RRArbiter`: runs in round-robin order

Note that Arbiter routing is implemented in **combinational logic**.

~~~scala
class MyArbiter(InNum: Int, width: Int) extends Module {
    // Example circuit using a priority arbiter
    val io = IO(new Bundle {
      val in = Flipped(Vec(InNum, Decoupled(UInt(width.W))))
      val out = Decoupled(UInt(width.W))
    })
    // Arbiter doesn't have a convenience constructor, so it's built like any Module
    val arbiter = Module(new Arbiter(UInt(width.W), InNum))  // 2 to 1 Priority Arbiter
    arbiter.io.in <> io.in
    io.out <> arbiter.io.out
}
println(getVerilog(new MyArbiter(2, 32)))
~~~

## PopCount

PopCount returns the number of high (1) bits in the input as a `UInt`.

计算 `1` 的个数。

~~~scala
io.out := PopCount(io.in)
~~~

## Reverse

Reverse returns the bit-reversed input.

翻转。

~~~scala
io.out := Reverse(io.in)
~~~

## OneHot encoding utilities

OneHot is an encoding of integers where there is one wire for each value, and exactly one wire is high. This allows the efficient creation of some functions, for example muxes. However, behavior may be undefined if the one-wire-high condition is not held.

- UInt to OneHot: `UIntToOH`
- OneHot to UInt: `OHToUInt`

## Muxes

These muxes take in a list of values with select signals, and output the value associated with the lowest-index select signal.

These can either take a list of (select: Bool, value: Data) tuples, or corresponding lists of selects and values as arguments. For simplicity, the examples below only demonstrate the second form.

### Priority Mux

A `PriorityMux` outputs the value associated with the lowest-index asserted select signal.

### OneHot Mux

An `Mux1H` provides an efficient implementation when it is guaranteed that exactly one of the select signals will be high. Behavior is undefined if the assumption is not true.

~~~scala
class MyPriorityMux(InNum: Int, width: Int) extends Module {
    // Example circuit using PriorityMux
    val io = IO(new Bundle {
      val in_sels = Input(Vec(InNum, Bool()))
      val in_bits = Input(Vec(InNum, UInt(width.W)))
      val out = Output(UInt(width.W))
    })
    io.out := PriorityMux(io.in_sels, io.in_bits)
}
println(getVerilog(new MyPriorityMux(2, 32)))
~~~

## counter

~~~scala
class MyCounter(cnt: Int, width: Int) extends Module {
    // Example circuit using Mux1H
    val io = IO(new Bundle {
      val count = Input(Bool())
      val out = Output(UInt(width.W))
    })
    val counter = Counter(cnt)  // 3-count Counter (outputs range [0...2])
    when(io.count) {
      counter.inc()
    }
    io.out := counter.value
  }

println(getVerilog(new MyCounter(3, 2))) // 3-count Counter (outputs range [0...2])
~~~

## Map

~~~scala
println(List(1, 2, 3, 4).map(x => x + 1))  // explicit argument list in function
println(List(1, 2, 3, 4).map(_ + 1))  // equivalent to the above, but implicit arguments
println(List(1, 2, 3, 4).map(_.toString + "a"))  // the output element type can be different from the input element type

println(List((1, 5), (2, 6), (3, 7), (4, 8)).map { case (x, y) => x*y })  // this unpacks a tuple, note use of curly braces

// Related: Scala has a syntax for constructing lists of sequential numbers
println(0 to 10)  // to is inclusive , the end point is part of the result
println(0 until 10)  // until is exclusive at the end, the end point is not part of the result

// Those largely behave like lists, and can be useful for generating indices:
val myList = List("a", "b", "c", "d")
println((0 until 4).map(myList(_)))
~~~

> ```
> List(2, 3, 4, 5)
> List(2, 3, 4, 5)
> List(1a, 2a, 3a, 4a)
> List(5, 12, 21, 32)
> Range 0 to 10
> Range 0 until 10
> Vector(a, b, c, d)
> ```

## **zipWithIndex**

~~~scala
println(List(1, 2, 3, 4).zipWithIndex)  // note indices start at zero
println(List("a", "b", "c", "d").zipWithIndex)
println(List(("a", "b"), ("c", "d"), ("e", "f"), ("g", "h")).zipWithIndex)  // tuples nest
~~~

> ```
> List((1,0), (2,1), (3,2), (4,3))
> List((a,0), (b,1), (c,2), (d,3))
> List(((a,b),0), ((c,d),1), ((e,f),2), ((g,h),3))
> ```

## **Reduce**

~~~scala
println(List(1, 2, 3, 4).reduce((a, b) => a + b))  // returns the sum of all the elements
println(List(1, 2, 3, 4).reduce(_ * _))  // returns the product of all the elements
println(List(1, 2, 3, 4).map(_ + 1).reduce(_ + _))  // you can chain reduce onto the result of a map
~~~

> ```
> 10
> 24
> 14
> ```

## **Fold**

类似 `reduce`，不过可以提供一个初值。

~~~scala
println(List(1, 2, 3, 4).fold(0)(_ + _))  // equivalent to the sum using reduce
println(List(1, 2, 3, 4).fold(1)(_ + _))  // like above, but accumulation starts at 1
println(List().fold(1)(_ + _))  // unlike reduce, does not fail on an empty input
~~~

> ```
> 10
> 11
> 1
> ```

## **Decoupled Arbiter**

~~~scala
class MyRoutingArbiter(numChannels: Int) extends Module {
  val io = IO(new Bundle {
    val in = Vec(numChannels, Flipped(Decoupled(UInt(8.W))))
    val out = Decoupled(UInt(8.W))
  } )

  // YOUR CODE BELOW
    io.out.valid := io.in.map(_.valid).reduce(_ || _)
    
  // 注意，这里是 = 而不是 :=
    val channel = PriorityMux(
        io.in.map(_.valid).zipWithIndex.map { case (valid, index) => (valid, index.U) }
    )
    
    for(i <- 0 until numChannels) {
        when(channel === i.U) {
            io.in(i).ready := io.out.ready
        }.otherwise{
            io.in(i).ready := 0.U
        }  
    }
// or    
//     io.in.map(_.ready).zipWithIndex.foreach { case (ready, index) =>
//         ready := io.out.ready && channel === index.U
//     }
    
    io.out.bits := io.in(channel).bits
}
~~~

## scala 语法

### 合并 list

Merge two lists using the `++`, `concat`, or `:::` methods. 

# Functional Programming

