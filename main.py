"""
🔥 ЮЛА БОТ PRO v5.0
Полный функционал для прогрева и публикации объявлений мототехники
"""

import sys
import asyncio
import random
from pathlib import Path
from datetime import datetime
from colorama import Fore, Back, Style, init

# Если нет файла config.py, создаём локально
try:
    from config import ACCOUNTS, WARMUP_CONFIG, STORAGE_DIR, REPORTS_DIR
except:
    ACCOUNTS = {}
    WARMUP_CONFIG = {}
    STORAGE_DIR = Path("./storage")
    REPORTS_DIR = STORAGE_DIR / "reports"

from core.logger import Logger
from core.anti_detect import AntiDetect
from accounts.account import YulaAccount

init(autoreset=True)

logger = Logger("YulaBot")
anti_detect = AntiDetect()

class YulaBotManager:
    """🔥 МЕНЕДЖЕР ВСЕХ БОТОВ"""
    
    def __init__(self):
        self.accounts = {}
        self.report_file = REPORTS_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        logger.success("✅ YulaBotManager инициализирован")
    
    def print_banner(self):
        """Красивый баннер"""
        banner = (
            f"\n{Fore.CYAN}{'='*120}{Style.RESET_ALL}\n"
            f"{Fore.YELLOW}{'🔥 ЮЛА БОТ PRO v5.0 - ПОЛНЫЙ ФУНКЦИОНАЛ':^120}{Style.RESET_ALL}\n"
            f"{Fore.YELLOW}{'Автоматический прогрев и управление аккаунтами':^120}{Style.RESET_ALL}\n"
            f"{Fore.CYAN}{'='*120}{Style.RESET_ALL}\n\n"
            f"{Fore.GREEN}Команды:{Style.RESET_ALL}\n"
            f"1. {Fore.YELLOW}login <номер>{Style.RESET_ALL}       - Вход в аккаунт (1-5)\n"
            f"2. {Fore.YELLOW}warmup <номер>{Style.RESET_ALL}      - Начать прогрев аккаунта\n"
            f"3. {Fore.YELLOW}stop <номер>{Style.RESET_ALL}        - Остановить прогрев\n"
            f"4. {Fore.YELLOW}close <номер>{Style.RESET_ALL}       - Закрыть браузер\n"
            f"5. {Fore.YELLOW}status{Style.RESET_ALL}              - Показать статус всех аккаунтов\n"
            f"6. {Fore.YELLOW}report{Style.RESET_ALL}              - Сохранить отчет\n"
            f"7. {Fore.YELLOW}help{Style.RESET_ALL}                - Справка\n"
            f"8. {Fore.YELLOW}exit{Style.RESET_ALL}                - Выход\n"
            f"\n{Fore.CYAN}{'='*120}{Style.RESET_ALL}\n"
        )
        print(banner)
    
    def print_status(self):
        """Вывести статус всех аккаунтов"""
        print(f"\n{Fore.CYAN}{'='*120}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'📊 СТАТУС АККАУНТОВ':^120}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*120}{Style.RESET_ALL}\n")
        
        if not self.accounts:
            print(f"{Fore.RED}❌ Нет активных аккаунтов{Style.RESET_ALL}\n")
            return
        
        for acc_id, account in self.accounts.items():
            report = account.get_status_report()
            
            print(f"{report['status']} {report['name']:<50}")
            print(f"   └─ Действий: {report['total_actions']:3d} | ✅: {report['successful_actions']:3d} | ❌: {report['failed_actions']:3d}")
            print(f"   └─ Фаз прогрева: {len(report['warmup_phases_completed'])}/4")
            print(f"   └─ Готов к публикации: {'✅ ДА' if report['ready_for_listing'] else '❌ НЕТ'}")
            print()
    
    async def login(self, account_number: int) -> bool:
        """🔐 Вход в аккаунт"""
        try:
            acc_id = f"account_{account_number}"
            
            if acc_id not in ACCOUNTS:
                logger.error(f"❌ Аккаунт #{account_number} не найден")
                return False
            
            if acc_id in self.accounts and self.accounts[acc_id].browser_manager.driver:
                logger.warning(f"⚠️  Аккаунт #{account_number} уже активен")
                return False
            
            logger.info(f"🔐 Вход в аккаунт #{account_number}...")
            
            account = YulaAccount(ACCOUNTS[acc_id], anti_detect)
            
            if await account.login_to_yula():
                self.accounts[acc_id] = account
                logger.success(f"✅ Вход в аккаунт #{account_number} успешен")
                return True
            else:
                logger.error(f"❌ Ошибка входа в аккаунт #{account_number}")
                account.close()
                return False
        
        except Exception as e:
            logger.error(f"❌ Исключение при входе: {e}")
            return False
    
    async def warmup(self, account_number: int) -> bool:
        """🔥 Начать прогрев"""
        try:
            acc_id = f"account_{account_number}"
            
            if acc_id not in self.accounts:
                logger.error(f"❌ Аккаунт #{account_number} не активирован")
                return False
            
            account = self.accounts[acc_id]
            
            logger.info(f"🔥 Начинаю прогрев аккаунта #{account_number}...")
            
            if await account.warmup(WARMUP_CONFIG.get('total_duration', 95)):
                logger.success(f"✅ Прогрев аккаунта #{account_number} завершён")
                return True
            else:
                logger.error(f"❌ Ошибка прогрева аккаунта #{account_number}")
                return False
        
        except Exception as e:
            logger.error(f"❌ Исключение при прогреве: {e}")
            return False
    
    async def stop(self, account_number: int):
        """⏹️ Остановить прогрев"""
        try:
            acc_id = f"account_{account_number}"
            
            if acc_id in self.accounts:
                self.accounts[acc_id].stop_warmup()
                logger.success(f"✅ Прогрев аккаунта #{account_number} остановлен")
            else:
                logger.error(f"❌ Аккаунт #{account_number} не найден")
        
        except Exception as e:
            logger.error(f"❌ Ошибка остановки: {e}")
    
    async def close(self, account_number: int):
        """🔒 Закрыть браузер"""
        try:
            acc_id = f"account_{account_number}"
            
            if acc_id in self.accounts:
                self.accounts[acc_id].close()
                del self.accounts[acc_id]
                logger.success(f"✅ Аккаунт #{account_number} закрыт")
            else:
                logger.error(f"❌ Аккаунт #{account_number} не найден")
        
        except Exception as e:
            logger.error(f"❌ Ошибка закрытия: {e}")
    
    async def save_report(self):
        """📋 Сохранить отчет"""
        try:
            with open(self.report_file, 'w', encoding='utf-8') as f:
                f.write(f"{'='*120}\n")
                f.write(f"{'ОТЧЕТ ЮЛА БОТ PRO v5.0':^120}\n")
                f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*120}\n\n")
                
                for acc_id, account in self.accounts.items():
                    report = account.get_status_report()
                    
                    f.write(f"{report['name']}\n")
                    f.write(f"{'-'*120}\n")
                    f.write(f"Статус: {report['status']}\n")
                    f.write(f"Действий: {report['total_actions']}\n")
                    f.write(f"Успешных: {report['successful_actions']}\n")
                    f.write(f"Ошибок: {report['failed_actions']}\n")
                    phases = ', '.join(report['warmup_phases_completed']) if report['warmup_phases_completed'] else "Не пройдено"
                    f.write(f"Фаз прогрева: {phases}\n")
                    f.write(f"Готов к публикации: {'ДА' if report['ready_for_listing'] else 'НЕТ'}\n\n")
                    
                    if report['recommendations']:
                        f.write(f"Рекомендации:\n")
                        for rec in report['recommendations']:
                            f.write(f"  {rec}\n")
                        f.write(f"\n")
            
            logger.success(f"✅ Отчет сохранён: {self.report_file}")
        
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения отчета: {e}")
    
    def show_help(self):
        """Показать справку"""
        help_text = (
            "\n📖 СПРАВКА\n\n"
            "ОСНОВНЫЕ КОМАНДЫ:\n"
            "─────────────────\n\n"
            "login <номер>\n"
            "    Вход в аккаунт (1-5)\n"
            "    Пример: login 1\n\n"
            "warmup <номер>\n"
            "    Начать полный прогрев аккаунта (95 минут)\n"
            "    Включает 4 фазы:\n"
            "      • Фаза 1: Прогрев браузера (15 мин)\n"
            "      • Фаза 2: Изучение Юлы (20 мин)\n"
            "      • Фаза 3: Настройка профиля (15 мин)\n"
            "      • Фаза 4: Просмотр объявлений (25 мин)\n"
            "    Пример: warmup 1\n\n"
            "stop <номер>\n"
            "    Остановить текущий прогрев\n"
            "    Пример: stop 1\n\n"
            "close <номер>\n"
            "    Закрыть браузер и сохранить куки\n"
            "    Пример: close 1\n\n"
            "status\n"
            "    Показать статус всех активных аккаунтов\n\n"
            "report\n"
            "    Сохранить подробный отчет в файл\n\n"
            "help\n"
            "    Показать эту справку\n\n"
            "exit\n"
            "    Выход из программы\n\n"
            "⚡ РЕКОМЕНДАЦИИ:\n"
            "─────────────────\n\n"
            "1. Сначала выполните login <номер> для каждого аккаунта\n"
            "2. Затем запустите warmup для каждого (они работают параллельно)\n"
            "3. После прогрева система сама скажет, когда публиковать объявление\n"
            "4. Не останавливайте браузер во время прогрева!\n"
            "5. Регулярно проверяйте status для мониторинга\n\n"
            "🔒 БЕЗОПАСНОСТЬ:\n"
            "─────────────────\n\n"
            "✅ Все куки автоматически сохраняются\n"
            "✅ Используется анти-детект система\n"
            "✅ Реалистичное поведение браузера\n"
            "✅ Случайные задержки между действиями\n"
            "✅ Разные User-Agents для каждого браузера\n"
        )
        print(help_text)
    
    async def run(self):
        """Главный цикл управления"""
        self.print_banner()
        print(f"{Fore.GREEN}Введите 'help' для справки{Style.RESET_ALL}\n")
        
        while True:
            try:
                command = input(f"\n{Fore.CYAN}➜ {Style.RESET_ALL}").strip().lower()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0]
                
                if cmd == "exit":
                    print(f"\n{Fore.YELLOW}Закрываю все браузеры...{Style.RESET_ALL}")
                    for acc_id in list(self.accounts.keys()):
                        await self.close(int(acc_id.split('_')[1]))
                    print(f"{Fore.GREEN}✅ До свидания!{Style.RESET_ALL}\n")
                    break
                
                elif cmd == "help":
                    self.show_help()
                
                elif cmd == "status":
                    self.print_status()
                
                elif cmd == "report":
                    await self.save_report()
                
                elif cmd == "login" and len(parts) > 1:
                    try:
                        acc_num = int(parts[1])
                        await self.login(acc_num)
                    except ValueError:
                        logger.error("❌ Укажите номер аккаунта (1-5)")
                
                elif cmd == "warmup" and len(parts) > 1:
                    try:
                        acc_num = int(parts[1])
                        await self.warmup(acc_num)
                    except ValueError:
                        logger.error("❌ Укажите номер аккаунта (1-5)")
                
                elif cmd == "stop" and len(parts) > 1:
                    try:
                        acc_num = int(parts[1])
                        await self.stop(acc_num)
                    except ValueError:
                        logger.error("❌ Укажите номер аккаунта (1-5)")
                
                elif cmd == "close" and len(parts) > 1:
                    try:
                        acc_num = int(parts[1])
                        await self.close(acc_num)
                    except ValueError:
                        logger.error("❌ Укажите номер аккаунта (1-5)")
                
                else:
                    logger.warning("⚠️  Неизвестная команда. Введите 'help' для справки")
            
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Прервано пользователем{Style.RESET_ALL}")
                break
            except Exception as e:
                logger.error(f"❌ Ошибка: {e}")

async def main():
    """Главная функция"""
    manager = YulaBotManager()
    await manager.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Выход{Style.RESET_ALL}\n")
        sys.exit(0)