
Table of Contents
=================

* [Mali Kuu Enterprises Data Generator](#mali-kuu-enterprises-data-generator)
   * [Installation](#installation)
   * [Usage](#usage)
      * [Populating Sample Data](#populating-sample-data)
   * [Contribution](#contribution)
   * [License](#license)

# Mali Kuu Enterprises Data Generator
This repository is an extension of the Mali Kuu Enterprises Repository, which is a stock and sales management system. This extension contains python scripts that populate sample data for the Mali Kuu Main Project. The purpose of these scripts is to help developers quickly set up test data in their Mali Kuu applications while familiarizing with the concepts.

## Installation
1. Clone the repository to your local machine:
```bash
git clone https://github.com/barasamichael/Mali_Kuu_Enterprises-Data_Generator.git
```
2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Configure your database settings in `config.py`.

## Usage
### Populating Sample Data
Ensure your database settings are properly configured in `config.py` <br>
From the root directory of the project, run the following command:
```bash
python generate_data.py
```
This command will populate the Mali Kuu database with sample data.

## Contribution
1. Fork the repository to your GitHub account.
2. Clone the repository to your local machine.

3. Create a new branch:
```bash
git checkout -b <branch-name>
```

4. Make the desired changes and commit:
```bash
git add .
git commit -m "commit-message"
```

5. Push your changes to GitHub:
```bash
git push origin <branch-name>
```

6. Create a Pull Request to the main branch.

## License
This project is licensed under the `GNU Public License` - see the `LICENSE` file for more details.
