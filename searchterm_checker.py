import numpy as np
import urllib

file_with_terms = 'Top 500 search terms.csv'      # File
column_with_terms = 0                             # Index of column, 0 is first

f = []
f123 = []
g = open(file_with_terms, 'r')

# LOAD IN terms
for x in g:
    f.append('http://www.lowes.com/Search={0}?langId=-1&N=0&newSearch=true&Ntt={}&view=list'.format(urllib.quote_plus(x.split(',')[column_with_terms].split('\n')[0])))
    f123.append(urllib.quote_plus(x.split(',')[column_with_terms].split('\n')[0]))
    
f123 = np.asarray(f123)[1:]                             # Store a copy of the term
f = np.asarray(f)[1:]                                   # Kills header

# ITERATE OVER SAMPLE
print 'TERM|URL|STATUS'
for i in range(np.size(f)):
    try:
        f1 = urllib.urlopen(f[i])
        g = f1.read()
        null_check = np.size(g.split('div class=\"search_noResults\"'))
        four_oh_four_check = np.size(g.split('requested file was not found'))
        lp_check = np.size(g.split('earch results for'))
        redirect_check = np.size(g.split('var URLAfterLogon = '))
        bad_result_check = np.size(g.split('<h1>Bad Request</h1>'))
        pd_check = np.size(g.split('<div class=\"itemInfo\">'))
        if null_check > 1:
            status = 'null_page'
        elif four_oh_four_check > 1:
            status = '404_error'
        elif lp_check > 1:
            status = 'list_page'
        elif pd_check > 1:
            status = 'product_detail'
        elif redirect_check > 1:
            prod_list_check = np.size(g.split('ProductListView'))
            cat_tolist_page_check = np.size(g.split('Sort by'))
            if prod_list_check > 1:
                status = 'redirect_list'
            elif (cat_tolist_page_check == 1):
                status = 'redirect_cat'
            else:
                status = 'redirect_unconfirmed'
        elif bad_result_check > 1:
            status = 'bad_result'
        else:
            status = 'unable_to_determine'
            # continue
        print '{0}|{1}|{2}'.format(f123[i],f[i],status)
    except:
        print '{0}^{1}^{2}'.format(f123[i],f[i],'error_with_html_input')
