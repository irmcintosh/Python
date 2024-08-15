# Password Generator

A Python-based password generator that converts a phrase into a secure password. This application provides options to add special characters to the generated password and evaluates its strength.

## Features

- Converts a user-provided phrase into a password by replacing specific characters.
- Adds special characters (`*` and `-`) at the beginning or end of the password.
- Evaluates the strength of the generated password.
- Allows users to copy the generated password to the clipboard.
- Allows users to save the generated password to a file.

## Requirements

- Python 3.11
- Tkinter (comes with Python)
- PyInstaller (for creating standalone executables)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/irmcintosh/passwordGen.git
    cd passwordGen
    ```

2. **Install required packages:**
    If you don't have PyInstaller installed, you can install it via pip:
    ```bash
    pip install pyinstaller
    ```

## Usage

### Running the Script

To run the script directly, navigate to the directory containing `passwordGen.py` and execute:

```bash
python passwordGen.py
```

### Creating a Standalone Executable

To create a standalone executable for Windows, use PyInstaller:

1. **Navigate to the script directory:**
    ```bash
    cd C:\Users\Ian12724\Desktop\passwordGen
    ```

2. **Set the Path to PyInstaller (if not already in PATH):**
    ```bash
    set PATH=%PATH%;C:\Users\Ian12724\AppData\Roaming\Python\Python311\Scripts
    ```

3. **Run PyInstaller:**
    ```bash
    pyinstaller --onefile --windowed passwordGen.py
    ```

The standalone executable will be created in the `dist` directory.

## Features

- **Enter Phrase**: Input a phrase that will be converted into a password.
- **Special Characters**: Options to add `*` or `-` at the beginning or end of the generated password.
- **Generate Password**: Generates the password based on the entered phrase and selected options.
- **Copy to Clipboard**: Copies the generated password to the clipboard.
- **Clear**: Clears the input fields and generated password.
- **Save to File**: Saves the generated password to a text file.

## Screenshots

![Password Generator](screenshots/password_generator.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## Acknowledgments

- Inspired by common password generation techniques and security best practices.
```

### How to Use

1. **Clone the repository to your local machine**.
2. **Save the above content into a file named `README.md` in the root directory of your project**.
3. **Add and commit the `README.md` file to your GitHub repository**.

```bash
git add README.md
git commit -m "Add README.md file"
git push origin main
```
