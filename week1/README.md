## Week1
[1주차 정리](https://www.notion.so/corcaai/f47f90c39ed8454db3e3822a7c2f4b39?pvs=4)

### Assignment
CPU, RAM, ROM으로 구성된 Computer를 구현합니다.

- CPU는 추상클래스입니다.
    - 일반적인 Factory 패턴으로 구현해 주세요.
    - CPUFactory에서 SingleCoreCPU, DoubleCoreCPU를 생성할 수 있습니다.
- RAM, ROM은 추상 클래스 Memory를 상속받습니다.
    - 각각은 Factory를 가지며, 각각의 Factory도 공통의 추상 클래스를 상속받게 Abstract factory 패턴으로 구현해 주세요.
- Computer는 Builder 패턴으로 구현해 주세요.
    - bootstrap을 하고 나면 아래 키를 가지는 dict 타입의 state를 반환합니다.
        - cpu processed
            - cpu가 process한 data list
        - ram(rom) data
            - ram(rom)의 현재 data

### Test 결과
`python -m pytest tests`
```
=== test session starts ===
platform linux -- Python 3.10.12, pytest-8.0.0, pluggy-1.4.0
rootdir: /home/taehyeon/EZ-DESIGN-study/week1/tests
configfile: pytest.ini

collected 9 items
tests/test_computer.py .........

=== 9 passed in 0.01s ===
```