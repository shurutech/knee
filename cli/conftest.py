from dotenv import load_dotenv, find_dotenv

def pytest_configure():
		load_dotenv(find_dotenv())