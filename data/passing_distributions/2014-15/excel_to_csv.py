# Jade Huang
# source: stackoverflow.com

import argparse
import xlrd
import csv
import re
import codecs
import cStringIO

class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        '''next() -> unicode
        This function reads and returns the next line as a Unicode string.
        '''
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        '''writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        '''
        ar = []
        for s in row:
        	if type(s) == float:
        		s = str(s)
        		if s[-2:] == ".0":
        			s = re.sub("\.0$", "", s)
        	ar.append(s.encode('utf-8'))
        self.writer.writerow(ar)
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        data = re.sub("\"", "", data)
        
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
			self.writerow(row)

parser = argparse.ArgumentParser(description="Convert xls to csv")
parser.add_argument('-xls', '-x', dest='xls', required = True)
parsed_args = parser.parse_args()

xls_name = parsed_args.xls
csv_name = re.sub("\.xlsx?$", "", xls_name) + ".csv"
csv_name = re.sub(".*\/", "", csv_name)
# print "xls: %s, csv: %s" % (xls_name, csv_name)


wb = xlrd.open_workbook(xls_name)
sh = wb.sheet_by_name('PDFTables.com')
directory = "csv/"
csv_file = open(directory+csv_name, 'wb')
# TODO: UnicodeEncodeError
# wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
wr = UnicodeWriter(csv_file, quoting=csv.QUOTE_ALL)

reader = UnicodeReader(sh)
for rownum in xrange(sh.nrows):
# for line in reader:
    # wr.writerow(sh.row_values(rownum))
    # print "row: ", sh.row_values(rownum)
    wr.writerow(sh.row_values(rownum))
csv_file.close()
