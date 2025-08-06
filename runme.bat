@echo off
chcp 65001 >nul
title Installation Extracteur de Palette de Couleurs

echo ================================
echo Extracteur de Palette de Couleurs
echo Script d'installation et de lancement
echo ================================

echo.
echo [1/4] Vérification de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

echo [2/4] Création de l'environnement virtuel...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERREUR: Impossible de créer l'environnement virtuel
    pause
    exit /b 1
)

echo [3/4] Activation de l'environnement virtuel et installation des dépendances...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERREUR: Impossible d'installer les dépendances
    pause
    exit /b 1
)

echo [4/4] Lancement de l'application...
echo.
echo L'application va démarrer dans quelques secondes...
echo Accédez à http://localhost:7860 dans votre navigateur
echo.
echo Pour arrêter l'application, fermez cette fenêtre ou appuyez sur CTRL+C
echo.

python app.py

if %errorlevel% neq 0 (
    echo ERREUR: Impossible de lancer l'application
    pause
    exit /b 1
)

echo ================================
echo Installation et lancement terminés !
echo ================================
pause