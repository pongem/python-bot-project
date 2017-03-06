# -*- coding: utf-8 -*-

from urllib2 import urlopen 
from decimal import Decimal
from BeautifulSoup import BeautifulSoup

from datetime import datetime

from string import ascii_lowercase

import re


class DayData:
    date = None
    open = None
    close = None
    max = None
    min = None
    volume = None
    value = None
    set_index = None

    def __init__(self):
        pass

    @staticmethod
    def to_datetime(str):
        from datetime import datetime
        ds = [int(x) for x in str.split('/')]
        ds[2] = ds[2] + 2000
        return datetime(ds[2], ds[1], ds[0])
                
    @staticmethod
    def to_decimal(str):
        from decimal import Decimal
        return Decimal(str.replace(',',''))

class SETFetch:

    def __init__(self):
        self.set_stockdata_url = "http://www.settrade.com/C04_02_stock_historical_p1.jsp?txtSymbol=%s&selectPage=null&max=15&offset=%d";
        self.set100_url = "http://www.settrade.com/C13_MarketSummary.jsp?detail=SET100"

        self.allset = "https://www.set.or.th/set/commonslookup.do?language=th&country=TH&prefix=%s"
        self.stockinfo = "https://marketdata.set.or.th/mkt/stockquotation.do?symbol=%s&ssoPageId=1"

    def fetchAllSet(self):
        arrResult = []
        for a_char in ascii_lowercase :
            url = self.allset % a_char

            page = urlopen( url )
            soup = BeautifulSoup(page )

            stocks = soup.findAll('a', href=re.compile('^/set/companyprofile.do(.*)'))

            for stock in stocks :
                if ( stock != None ):
                    arrResult.append( stock.text.upper() )

        return arrResult

    def fetchSet100(self):
        page = urlopen(self.set100_url)
        soup = BeautifulSoup(page )

        stocks = soup.findAll("a", {"class": "link-stt"})

        arrSTocks = []
        for stock in stocks :
            if (stock.text.find("SET") < 0):
                #print( stock.text )
                arrSTocks.append( stock.text.upper() )
        return arrSTocks

    def fetchCurrentStockInfo(self,symbol):
        oStockInfo = {}

        page = urlopen( self.stockinfo % symbol )
        print ( "url %s" %(self.stockinfo % symbol)) 

        soup = BeautifulSoup( page )

        pricetags = soup.findAll( "td", style=re.compile('bold') )

        for pricetag in pricetags :
            cur_price = pricetag.text

            try:
                return float( cur_price )
            except:
                return None


        return None



    def fetchDataStock(self,symbol):
        
        cur_pos = 0
        all_data = []

        while True:
            #print ( self.set_stockdata_url % (symbol, cur_pos * 15) )
            page = urlopen( self.set_stockdata_url % (symbol, cur_pos * 15))
            soup = BeautifulSoup(page)

            # need code this change if settrade change to display data more than 15
            # get content body
            read_data = None
            contents = soup.findAll( 'tbody' )
            for content in contents :
                body = content.findAll('tr')
                if ( len (body) == 15 ) :
                    read_data = body
                    #print("Grab it!")

            if read_data == None:
                # no more data to read
                break
            cur_pos = cur_pos + 1
            all_data = all_data + read_data

        daily = []
        for day in all_data:
            flds = day.findAll('td')
            current = DayData()
            try:
                current.date =  DayData.to_datetime(flds[0].text)
                current.open = DayData.to_decimal(flds[1].text)
                current.max = DayData.to_decimal(flds[2].text)
                current.min = DayData.to_decimal(flds[3].text)
                current.close = DayData.to_decimal(flds[5].text)
                current.volume = DayData.to_decimal(flds[8].text) * 1000
                current.value = DayData.to_decimal(flds[9].text)
                current.set_index = DayData.to_decimal(flds[10].text)
                daily.append(current) 
            except Exception as e:
                print ("error formatting data")
                pass
            finally:
                pass
        daily.sort(key=lambda x: x.date, reverse=True)
        return daily


class SetData:
    # last update march 6, 2017
    # can be update by SETFetch.fetchAllSet
    arrAllSets = [u'A', u'AAV', u'ABC', u'ABICO', u'ABPIF', u'ACAP', u'ACC', u'ADAM', u'ADVANC', u'AEC', u'AEONTS', u'AF', u'AFC', u'AGE', u'AH', u'AHC', u'AI', u'AIE', u'AIRA', u'AIT', u'AJ', u'AJD', u'AKP', u'AKR', u'ALLA', u'ALT', u'ALUCON', u'AMA', u'AMANAH', u'AMARIN', u'AMATA', u'AMATAR', u'AMATAV', u'AMC', u'ANAN', u'AOT', u'AP', u'APCO', u'APCS', u'APURE', u'APX', u'AQ', u'AQUA', u'ARIP', u'ARROW', u'AS', u'ASEFA', u'ASIA', u'ASIAN', u'ASIMAR', u'ASK', u'ASN', u'ASP', u'ATP30', u'AU', u'AUCT', u'AYUD', u'BA', u'BAFS', u'BANPU', u'BAT-3K', u'BAY', u'BBL', u'BCH', u'BCP', u'BCPG', u'BDMS', u'BEAUTY', u'BEC', u'BEM', u'BFIT', u'BGT', u'BH', u'BIG', u'BIGC', u'BIZ', u'BJC', u'BJCHI', u'BKD', u'BKI', u'BKKCP', u'BLA', u'BLAND', u'BLISS', u'BM', u'BOL', u'BPP', u'BR', u'BRC', u'BROCK', u'BROOK', u'BRR', u'BSBM', u'BSM', u'BTC', u'BTNC', u'BTS', u'BTSGIF', u'BTW', u'BUI', u'BWG', u'CBG', u'CCET', u'CCN', u'CCP', u'CEN', u'CENTEL', u'CFRESH', u'CGD', u'CGH', u'CHARAN', u'CHEWA', u'CHG', u'CHO', u'CHOTI', u'CHOW', u'CHUO', u'CI', u'CIG', u'CIMBT', u'CITY', u'CK', u'CKP', u'CM', u'CMO', u'CMR', u'CNS', u'CNT', u'COL', u'COLOR', u'COM7', u'COMAN', u'CPALL', u'CPF', u'CPH', u'CPI', u'CPL', u'CPN', u'CPNCG', u'CPNRF', u'CPR', u'CPTGF', u'CRANE', u'CRYSTAL', u'CSC', u'CSL', u'CSP', u'CSR', u'CSS', u'CTARAF', u'CTW', u'CWT', u'DAII', u'DCC', u'DCON', u'DCORP', u'DELTA', u'DEMCO', u'DIF', u'DIMET', u'DNA', u'DRACO', u'DRT', u'DSGT', u'DTAC', u'DTC', u'DTCI', u'DTCPF', u'EA', u'EARTH', u'EASON', u'EASTW', u'ECF', u'ECL', u'EE', u'EFORL', u'EGATIF', u'EGCO', u'EIC', u'EKH', u'EMC', u'EPCO', u'EPG', u'ERW', u'ERWPF', u'ESSO', u'ESTAR', u'ETE', u'EVER', u'F&AMP;D', u'FANCY', u'FC', u'FE', u'FER', u'FMT', u'FN', u'FNS', u'FOCUS', u'FORTH', u'FPI', u'FSMART', u'FSS', u'FUTUREPF', u'FVC', u'GBX', u'GC', u'GCAP', u'GEL', u'GENCO', u'GFPT', u'GIFT', u'GJS', u'GL', u'GLAND', u'GLOBAL', u'GLOW', u'GOLD', u'GOLDPF', u'GPSC', u'GRAMMY', u'GRAND', u'GREEN', u'GSTEL', u'GTB', u'GUNKUL', u'GVREIT', u'GYT', u'HANA', u'HARN', u'HFT', u'HMPRO', u'HOTPOT', u'HPF', u'HPT', u'HREIT', u'HTC', u'HTECH', u'HYDRO', u'ICC', u'ICHI', u'IEC', u'IFEC', u'IFS', u'IHL', u'ILINK', u'IMPACT', u'INET', u'INOX', u'INSURE', u'INTUCH', u'IRC', u'IRCP', u'IRPC', u'IT', u'ITD', u'ITEL', u'IVL', u'J', u'JAS', u'JASIF', u'JCP', u'JCT', u'JMART', u'JMT', u'JSP', u'JTS', u'JUBILE', u'JUTHA', u'JWD', u'K', u'KAMART', u'KASET', u'KBANK', u'KBS', u'KC', u'KCAR', u'KCE', u'KCM', u'KDH', u'KGI', u'KIAT', u'KKC', u'KKP', u'KOOL', u'KPNPF', u'KSL', u'KTB', u'KTC', u'KTECH', u'KTIS', u'KWC', u'KWG', u'KYE', u'L&AMP;E', u'LALIN', u'LANNA', u'LDC', u'LEE', u'LH', u'LHBANK', u'LHHOTEL', u'LHK', u'LHPF', u'LHSC', u'LIT', u'LOXLEY', u'LPH', u'LPN', u'LRH', u'LST', u'LTX', u'LUXF', u'LVT', u'M', u'M-CHAI', u'M-II', u'M-PAT', u'M-STOR', u'MACO', u'MAJOR', u'MAKRO', u'MALEE', u'MANRIN', u'MATCH', u'MATI', u'MAX', u'MBAX', u'MBK', u'MBKET', u'MC', u'MCOT', u'MCS', u'MDX', u'MEGA', u'METCO', u'MFC', u'MFEC', u'MGT', u'MIDA', u'MILL', u'MINT', u'MIPF', u'MIT', u'MJD', u'MJLF', u'MK', u'ML', u'MNIT', u'MNIT2', u'MNRF', u'MODERN', u'MONO', u'MONTRI', u'MOONG', u'MPG', u'MPIC', u'MSC', u'MTI', u'MTLS', u'NBC', u'NC', u'NCH', u'NCL', u'NDR', u'NEP', u'NETBAY', u'NEW', u'NEWS', u'NFC', u'NINE', u'NKI', u'NMG', u'NNCL', u'NOBLE', u'NOK', u'NPK', u'NPP', u'NSI', u'NTV', u'NUSA', u'NWR', u'NYT', u'OCC', u'OCEAN', u'OGC', u'OHTL', u'OISHI', u'ORI', u'OTO', u'PACE', u'PAE', u'PAF', u'PAP', u'PATO', u'PB', u'PCA', u'PCSGH', u'PDG', u'PDI', u'PE', u'PERM', u'PF', u'PG', u'PHOL', u'PICO', u'PIMO', u'PJW', u'PK', u'PL', u'PLANB', u'PLAT', u'PLE', u'PM', u'PMTA', u'POLAR', u'POMPUI', u'POPF', u'POST', u'PPF', u'PPM', u'PPP', u'PPS', u'PR', u'PRAKIT', u'PRANDA', u'PREB', u'PRECHA', u'PRG', u'PRIN', u'PRINC', u'PRO', u'PSH', u'PSL', u'PSTC', u'PT', u'PTG', u'PTL', u'PTT', u'PTTEP', u'PTTGC', u'PYLON', u'Q-CON', u'QH', u'QHHR', u'QHOP', u'QHPF', u'QLT', u'QTC', u'RAM', u'RATCH', u'RCI', u'RCL', u'RICH', u'RICHY', u'RJH', u'RML', u'ROBINS', u'ROCK', u'ROH', u'ROJNA', u'RP', u'RPC', u'RPH', u'RS', u'RWI', u'S', u'S &AMP; J', u'S11', u'SABINA', u'SAFARI', u'SALEE', u'SAM', u'SAMART', u'SAMCO', u'SAMTEL', u'SANKO', u'SAPPE', u'SAT', u'SAUCE', u'SAWAD', u'SAWANG', u'SBPF', u'SC', u'SCB', u'SCC', u'SCCC', u'SCG', u'SCI', u'SCN', u'SCP', u'SE', u'SE-ED', u'SEAFCO', u'SEAOIL', u'SELIC', u'SENA', u'SF', u'SFP', u'SGF', u'SGP', u'SHANG', u'SIAM', u'SIM', u'SIMAT', u'SINGER', u'SIRI', u'SIRIP', u'SIS', u'SITHAI', u'SKR', u'SLP', u'SMART', u'SMIT', u'SMK', u'SMM', u'SMPC', u'SMT', u'SNC', u'SNP', u'SOLAR', u'SORKON', u'SPA', u'SPACK', u'SPALI', u'SPC', u'SPCG', u'SPF', u'SPG', u'SPI', u'SPORT', u'SPPT', u'SPRC', u'SPVI', u'SQ', u'SR', u'SRICHA', u'SRIPANWA', u'SSC', u'SSF', u'SSI', u'SSPF', u'SSSC', u'SST', u'SSTPF', u'SSTSS', u'STA', u'STANLY', u'STAR', u'STEC', u'STHAI', u'STPI', u'SUC', u'SUPER', u'SUSCO', u'SUTHA', u'SVH', u'SVI', u'SVOA', u'SWC', u'SYMC', u'SYNEX', u'SYNTEC', u'T', u'TACC', u'TAE', u'TAKUNI', u'TAPAC', u'TASCO', u'TBSP', u'TC', u'TCAP', u'TCB', u'TCC', u'TCCC', u'TCIF', u'TCJ', u'TCMC', u'TCOAT', u'TEAM', u'TF', u'TFD', u'TFG', u'TFI', u'TFUND', u'TGCI', u'TGPRO', u'TGROWTH', u'TH', u'THAI', u'THANA', u'THANI', u'THCOM', u'THE', u'THIF', u'THIP', u'THL', u'THRE', u'THREL', u'TIC', u'TICON', u'TIF1', u'TIP', u'TIPCO', u'TISCO', u'TIW', u'TK', u'TKN', u'TKS', u'TKT', u'TLGF', u'TLHPF', u'TLOGIS', u'TLUXE', u'TM', u'TMB', u'TMC', u'TMD', u'TMI', u'TMILL', u'TMT', u'TMW', u'TNDT', u'TNH', u'TNITY', u'TNL', u'TNP', u'TNPC', u'TNPF', u'TNR', u'TOG', u'TOP', u'TOPP', u'TPA', u'TPAC', u'TPBI', u'TPCH', u'TPCORP', u'TPIPL', u'TPOLY', u'TPP', u'TPRIME', u'TR', u'TRC', u'TREIT', u'TRIF', u'TRITN', u'TRT', u'TRU', u'TRUBB', u'TRUE', u'TSC', u'TSE', u'TSF', u'TSI', u'TSR', u'TSTE', u'TSTH', u'TTA', u'TTCL', u'TTI', u'TTL', u'TTLPF', u'TTTM', u'TTW', u'TU', u'TU-PF', u'TUCC', u'TVD', u'TVI', u'TVO', u'TVT', u'TWP', u'TWPC', u'TWZ', u'TYCN', u'U', u'UAC', u'UBIS', u'UEC', u'UKEM', u'UMI', u'UMS', u'UNIPF', u'UNIQ', u'UOBKH', u'UP', u'UPA', u'UPF', u'UPOIC', u'URBNPF', u'UREKA', u'UT', u'UTP', u'UV', u'UVAN', u'UWC', u'VARO', u'VGI', u'VI', u'VIBHA', u'VIH', u'VNG', u'VNT', u'VPO', u'VTE', u'WACOAL', u'WAVE', u'WG', u'WHA', u'WHABT', u'WHAPF', u'WHART', u'WICE', u'WIIK', u'WIN', u'WINNER', u'WORK', u'WORLD', u'WP', u'WR', u'XO', u'YCI', u'YNP', u'YUASA', u'ZMICO']


    def isStockInSet(self, stock):
        stock = stock.upper()
        if stock in self.arrAllSets :
            return True
        else:
            return False

