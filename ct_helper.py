import random

from utils import click_action


def select_patient() -> None:
    """
    随机选择患者类型
    :return:
    """
    choice = random.randint(0, 3)
    # print(choice)
    if choice == 0:
        click_action(201, 384, duration=0.5, wait=0.5)
    elif choice == 1:
        click_action(289, 384, duration=0.5, wait=0.5)
    else:
        click_action(374, 384, duration=0.5, wait=0.5)


def select_body_type() -> None:
    """
    随机选择患者体型
    :return:
    """
    choice = random.randint(0, 3)
    # print(choice)
    if choice == 0:
        click_action(201, 498, duration=0.5, wait=0.5)
    elif choice == 1:
        click_action(289, 498, duration=0.5, wait=0.5)
    else:
        click_action(374, 498, duration=0.5, wait=0.5)


def select_electricity() -> None:
    """
    随机调整电压电流
    :return:
    """
    u = random.randint(0, 5)
    for _ in range(u):
        click_action(198, 577)
    il = random.randint(0, 3)
    for _ in range(il):
        click_action(198, 617)
    ir = random.randint(0, 5)
    for _ in range(ir):
        click_action(374, 617)


def select_electricity_min() -> None:
    """
    调整电压电流到最小
    :return:
    """
    for _ in range(5):
        click_action(198, 577)
    for _ in range(3):
        click_action(198, 617)


def select_rebuild_model() -> None:
    """
    随机选择重建模式
    :return:
    """
    choice = random.randint(0, 2)
    if choice == 0:
        click_action(188, 841)
    else:
        click_action(331, 841)
