#coding:utf8
#!/usr/bin/python3
import sys
import csv
import os
import shutil

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import FirefoxProfile

el_by_xpath = lambda dr,xp: dr.wait.until( EC.presence_of_element_located((By.XPATH, xp)) )

def init_driver():
    """
    Se inicializa el driver de selenium
    con parametros específicos
    """
    fp = FirefoxProfile()
    fp.set_preference("browser.download.folderList",2)
    fp.set_preference("browser.download.manager.showWhenStarting",False)
    fp.set_preference("browser.download.dir",os.getcwd())
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk","text/plain")
    driver = webdriver.Firefox(firefox_profile=fp)
    driver.wait = WebDriverWait(driver, 5)
    return driver

def org_ncbi(dr):
    """
    Recibe un driver de selenium y regresa un elemento que corresponda
    a la entrada del organismo buscado en la página de KEGG
    """
    kegg_seq_xpath = "/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[13]/td[2]/a"
    el = el_by_xpath(dr,kegg_seq_xpath)
    return el

def get_fasta(dr,tipo="coding"):
    """
    Se busca la página correspondiente de ncbi al organismo en la de KEGG
    Regresa un elemento para hacer la descarga
    """
    ncbi_send_to_xpath = "/html/body/div[1]/div[1]/form/div[1]/div[5]/div/div[1]/h4/a"
    el = el_by_xpath(dr,ncbi_send_to_xpath)
    el.click()
    #especificamos "coding sequence"
    coding_xpath = '//*[@id="codeseq"]'
    el = el_by_xpath(dr,coding_xpath)
    el.click()
    #boton para bajar coding
    boton_xpath = "/html/body/div[1]/div[1]/form/div[1]/div[5]/div/div[1]/div[2]/div[2]/button"
    el = el_by_xpath(dr, boton_xpath)
    return el

get_idncbi = lambda s: s.split("/")[-1]

if __name__=='__main__':
    liga = sys.argv[1]
    dr = init_driver()
    dr.get(liga)
    url_actual = dr.current_url
    ncbi_id = get_idncbi(url_actual)
    el = org_ncbi(dr)
    el.click()   #pagina de ncbi
    el = get_fasta(dr,"coding")
    el.click()   #se baja el fasta en Downloads
    os.rename("./sequence.txt", "./"+ncbi_id+"_coding.fasta")
    dr.close()
