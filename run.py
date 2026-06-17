import subprocess
import sys
import os

def check_and_install_once():
    """Проверяет библиотеки только при первом запуске"""
    
    # Файл-маркер, который означает, что проверка уже выполнена
    marker_file = '.packages_installed'
    
    # Если файл-маркер существует, пропускаем проверку
    if os.path.exists(marker_file):
        print("✅ Библиотеки уже проверены ранее, пропускаем...")
        return
    
    print("📦 Первый запуск: проверяю и устанавливаю библиотеки...")
    
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_bcrypt',
        'flask_wtf',
        'email_validator',
        'python_dotenv'
    ]
    
    missing_packages = []
    
    # Проверяем наличие каждого пакета
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package} найден")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package} отсутствует")
    
    # Устанавливаем недостающие
    if missing_packages:
        print(f"\n📦 Устанавливаю: {', '.join(missing_packages)}")
        for package in missing_packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])
        print("✅ Все библиотеки установлены!")
    else:
        print("✅ Все библиотеки уже есть!")
    
    # Создаём файл-маркер, чтобы при следующем запуске не проверять
    with open(marker_file, 'w') as f:
        f.write('packages_installed')
    
    print("✅ Проверка выполнена. При следующих запусках проверяться не будет.\n")

# Запускаем проверку только один раз (при первом запуске)
if __name__ == '__main__':
    check_and_install_once()
    
    from app import create_app
    app = create_app()
    app.run(debug=True)