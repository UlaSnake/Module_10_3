import threading
import random
import time


class Bank:
    def __init__(self):
        """
        Инициализация класса Bank.
        Устанавливаем начальный баланс и создаем объект Lock для блокировки потоков.
        """
        self.balance = 0  # Начальный баланс банка
        self.lock = threading.Lock()  # Создаем объект Lock для синхронизации потоков

    def deposit(self):
        """
        Метод для пополнения баланса.
        Выполняет 100 транзакций пополнения средств.
        """
        for _ in range(100):  # Цикл для 100 транзакций
            amount = random.randint(50, 500)  # Генерируем случайное число от 50 до 500

            self.lock.acquire()  # Блокируем доступ к ресурсу
            self.balance += amount  # Увеличиваем баланс
            print(f"Пополнение: {amount}. Баланс: {self.balance}")  # Выводим информацию о пополнении

            # Проверяем, если баланс больше или равен 500
            if self.balance >= 500:
                print("Баланс достиг 500 или более, разблокировка.")
                self.lock.release()  # Разблокируем замок, если необходимо
            else:
                self.lock.release()  # Разблокируем замок, если не достигли порога

            time.sleep(0.001)  # Ожидание в 0.001 секунды

    def take(self):
        """
        Метод для снятия средств с баланса.
        Выполняет 100 транзакций снятия средств.
        """
        for _ in range(100):  # Цикл для 100 транзакций
            amount = random.randint(50, 500)  # Генерируем случайное число от 50 до 500

            print(f"Запрос на {amount}")  # Выводим запрос на снятие

            self.lock.acquire()  # Блокируем доступ к ресурсу
            if amount <= self.balance:  # Проверяем, достаточно ли средств на балансе
                self.balance -= amount  # Уменьшаем баланс
                print(f"Снятие: {amount}. Баланс: {self.balance}")  # Выводим информацию о снятии
                self.lock.release()  # Разблокируем замок после успешного снятия
            else:
                print("Запрос отклонён, недостаточно средств")  # Сообщаем об отказе в снятии
                self.lock.release()  # Разблокируем замок, если недостаточно средств

            time.sleep(0.001)  # Ожидание в 0.001 секунды


# Создаем объект класса Bank
bk = Bank()

# Создаем потоки для методов deposit и take
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

# Запускаем потоки
th1.start()
th2.start()

# Ожидаем завершения потоков
th1.join()
th2.join()

# Выводим итоговый баланс после завершения всех операций
print(f'Итоговый баланс: {bk.balance}')