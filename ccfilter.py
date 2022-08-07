import argparse
import csv
import json
from datetime import datetime
from typing import List
import requests as requests

ccf_ca = {'type': 'ca',
          'venues': (
	          'PPoPP', 'FAST', 'DAC', 'HPCA', 'MICRO', 'SC', 'ASPLOS', 'ISCA', 'USENIX ATC', 'SIGCOMM', 'MobiCom',
	          'INFOCOM',
	          'NSDI',
	          'CCS', 'EUROCRYPT', 'S&P', 'CRYPTO', 'USENIX Security', 'PLDI', 'POPL', 'FSE/ESEC', 'SOSP', 'OOPSLA',
	          'ASE', 'ICSE',
	          'ISSTA', 'OSDI', 'SIGMOD', 'SIGKDD', 'ICDE', 'SIGIR', 'VLDB', 'STOC', 'SODA', 'CAV', 'FOCS', 'LICS',
	          'ACM MM',
	          'SIGGRAPH', 'VR', 'IEEE VIS', 'AAAI', 'NeurIPS', 'ACL', 'CVPR', 'ICCV', 'ICML', 'IJCAI', 'CSCW', 'CHI',
	          'UbiComp',
	          'WWW', 'RTSS')}

ccf_ja = {'type': 'ja',
          'venues': (
	          'TOCS', 'TOS', 'TCAD', 'TC', 'TPDS', 'JSAC', 'TMC', 'TON', 'TITF', 'TDSC', 'TOPLAS', 'TOSEM', 'TSE',
	          'TODS', 'TOIS',
	          'TKDE', 'VLDBJ', 'TIT', 'IANDC', 'SICOMP', 'TOG', 'TIP', 'TVCG', 'AI', 'TPAMI', 'IJCV', 'JMLR', 'TOCHI',
	          'IJHCS',
	          'JACM', 'Proc. IEEE')}

ccf_cb = {'type': 'cb',
          'venues': (
	          'SoCC', 'SPAA', 'PODC', 'FPGA', 'CGO', 'DATE', 'EuroSys', 'HOT CHIPS', 'CLUSTER', 'ICCD', 'ICCAD',
	          'ICDCS',
	          'CODES+ISSS', 'HiPEAC', 'SIGMETRICS', 'PACT', 'ICPP', 'ICS', 'VEE', 'IPDPS', 'Performance', 'HPDC', 'ITC',
	          'LISA', 'MSST', 'RTAS', 'SenSys', 'CoNEXT', 'SECON', 'IPSN', 'MobiSys', 'ICNP', 'MobiHoc', 'NOSSDAV',
	          'IWQoS', 'IMC', 'ACSAC', 'ASIACRYPT', 'ESORICS', 'FSE', 'CSFW', 'SRDS', 'CHES', 'DSN', 'RAID', 'PKC',
	          'NDSS',
	          'TCC', 'ECOOP', 'ETAPS', 'ICPC', 'RE', 'CAiSE', 'ICFP', 'LCTES', 'MoDELS', 'CP', 'ICSOC', 'SANER',
	          'ICSME',
	          'VMCAI', 'ICWS', 'Middleware', 'SAS', 'ESEM', 'FM', 'ISSRE', 'HotOS', 'CIKM', 'WSDM', 'PODS', 'DASFAA',
	          'ECML-PKDD', 'ISWC', 'ICDM', 'ICDT', 'EDBT', 'CIDR', 'SDM', 'SoCG', 'ESA', 'CCC', 'ICALP', 'CADE/IJCAR',
	          'CONCUR', 'HSCC', 'SAT', 'ICMR', 'SI3D', 'SCA', 'DCC', 'EG', 'EuroVis', 'SGP', 'EGSR', 'ICASSP', 'ICME',
	          'ISMAR', 'PG', 'SPM', 'COLT', 'EMNLP', 'ECAI', 'ECCV', 'ICRA', 'ICAPS', 'ICCBR', 'COLING', 'KR', 'UAI',
	          'AAMAS', 'PPSN', 'GROUP', 'IUI', 'ITS', 'UIST', 'ECSCW', 'PERCOM', 'MobileHCI', 'CogSci', 'BIBM',
	          'EMSOFT',
	          'ISMB', 'RECOMB')}

ccf_jb = {'type': 'jb',
          'venues': (
	          'TACO', 'TAAS', 'TODAES', 'TECS', 'TRETS', 'TVLSI', 'JPDC', 'JSA', 'PARCO', 'TOIT', 'TOMCCAP', 'TOSN',
	          'CN', 'TCOM',
	          'TWC', 'TOPS', 'JCS', 'ASE', 'ESE', 'TSC', 'IETS', 'IST', 'JFP', 'JSS', 'RE', 'SCP', 'SoSyM', 'STVR',
	          'SPE', 'TKDD',
	          'TWEB', 'AEI', 'DKE', 'DMKD', 'EJIS', 'IPM', 'IS', 'JASIST', 'JWS', 'KAIS', 'TALG', 'TOCL', 'TOMS',
	          'Algorithmica',
	          'CC', 'FAC', 'FMSD', 'INFORMS', 'JCSS', 'JGO', 'JSC', 'MSCS', 'TCS', 'TOMCCAP', 'CAGD', 'CGF', 'CAD',
	          'GM', 'TCSVT',
	          'TMM', 'JASA', 'SIIMS', 'Speech Com', 'TAP', 'TSLP', 'AAMAS', 'CVIU', 'DKE', 'TAC', 'TASLP', 'TEC', 'TFS',
	          'TNNLS',
	          'IJAR', 'JAIR', 'JSLHR', 'PR', 'CSCW', 'HCI', 'IWC', 'IJHCI', 'UMUAI', 'Cognition', 'TASAE', 'TGARS',
	          'TITS', 'TMI',
	          'TR', 'TCBB', 'JCST', 'JAMIA')}

ccf_cc = {'type': 'cc',
          'venues': (
	          'CF', 'SYSTOR', 'NOCS', 'ASAP', 'ASP-DAC', 'Euro-Par', 'ETS', 'FPL', 'FCCM', 'GLSVLSI', 'ATS', 'HPCC',
	          'HiPC',
	          'MASCOTS', 'ISPA', 'CCGRID', 'NPC', 'ICA3PP', 'CASES', 'FPT', 'ICPADS', 'ISCAS', 'ISLPED', 'ISPD', 'HotI',
	          'VTS',
	          'ANCS', 'APNOMS', 'FORTE', 'LCN', 'GLOBECO M', 'ICC', 'ICCCN', 'MASS', 'P2P', 'IPCCC', 'WoWMoM', 'ISCC',
	          'WCNC',
	          'Networking', 'IM', 'MSN', 'MSWiM', 'WASA', 'HotNets', 'WiSec', 'SACMAT', 'DRM', 'IH&MMSec', 'ACNS',
	          'AsiaCCS',
	          'ACISP',
	          'CT-RSA', 'DIMVA', 'DFRWS', 'FC', 'TrustCom', 'SEC', 'IFIP WG 11.9', 'ISC', 'ICDF2C', 'ICICS',
	          'SecureComm', 'NSPW',
	          'PAM', 'PETS', 'SAC', 'SOUPS', 'HotSec', 'PEPM', 'PASTE', 'APLAS', 'APSEC', 'EASE', 'ICECCS', 'ICST',
	          'ISPASS',
	          'SCAM',
	          'COMPSAC', 'ICFEM', 'TOOLS', 'SCC', 'ICSSP', 'SEKE', 'QRS', 'ICSR', 'ICWE', 'SPIN', 'ATVA', 'LOPSTR',
	          'TASE', 'MSR',
	          'REFSQ', 'WICSA', 'APWeb', 'DEXA', 'ECIR', 'ESWC', 'WebDB', 'ER', 'MDM', 'SSDBM', 'WAIM', 'SSTD', 'PAKDD',
	          'WISE',
	          'CSL', 'FMCAD', 'FSTTCS', 'DSAA', 'ICTAC', 'IPCO', 'RTA', 'ISAAC', 'MFCS', 'STACS', 'CASA', 'CGI',
	          'INTERSPEECH',
	          'GMP',
	          'PacificVis', '3DV', 'CAD/Graphics', 'ICIP', 'MMM', 'PCM', 'SMI', 'AISTATS', 'ACCV', 'ACML', 'BMVC',
	          'NLPCC',
	          'CoNLL',
	          'GECCO', 'ICTAI', 'IROS', 'ALT', 'ICANN', 'FG', 'ICDAR', 'ILP', 'KSEM', 'ICONIP', 'ICPR', 'ICB', 'IJCNN',
	          'PRICAI',
	          'NAACL', 'DIS', 'ICMI', 'ASSETS', 'GI', 'UIC', 'INTERACT', 'IDC', 'CollaborateCom', 'CSCWD', 'CoopIS',
	          'MobiQuitous',
	          'AVI', 'AMIA', 'APBC', 'SMC', 'COSIT', 'ISBRA')}

ccf_jc = {'type': 'jc',
          'venues': (
	          'JETC', 'DC', 'FGCS', 'TCC', 'Integration', 'JETTA', 'JGC', 'MICPRO', 'RTS', 'TJSC', 'CC', 'TNSM', 'JNCA',
	          'MONET',
	          'PPNA', 'WCMC', 'CLSR', 'IMCS', 'IJICS', 'IJISP', 'JISA', 'SCN', 'CL', 'IJSEKE', 'STTT', 'JLAP', 'JWE',
	          'SOCA',
	          'SQJ',
	          'TPLP', 'DPD', 'I&M', 'IPL', 'IR', 'IJCIS', 'IJGIS', 'IJIS', 'IJKM', 'IJSWIS', 'JCIS', 'JDM', 'JGITM',
	          'JIIS',
	          'JSIS',
	          'ACTA', 'APAL', 'DAM', 'FUIN', 'LISP', 'IPL', 'JCOMPLEXITY', 'LOGCOM', 'JSL', 'LMCS', 'SIDMA', 'CGTA',
	          'CAVW',
	          'C&G',
	          'DCG', 'SPL', 'IET-IPR', 'JVCIR', 'MS', 'MTA', 'SPIC', 'TVC', 'TALLIP', 'AIM', 'DSS', 'EAAI', 'ESWA',
	          'TG',
	          'IET-CVI',
	          'IVC', 'IDA', 'IJCIA', 'IJIS', 'IJNS', 'IJPRAI', 'IJUFKS', 'IJDAR', 'JETAI', 'KBS', 'NLE', 'NCA', 'NPL',
	          'PAA',
	          'PRL',
	          'WI', 'BIT', 'PUC', 'PMC', 'FCS', 'JBHI', 'TBD', 'JBI')}

# 名称到元组的映射
ccf = {
	'ca': ccf_ca,
	'cb': ccf_cb,
	'cc': ccf_cc,
	'ja': ccf_ja,
	'jb': ccf_jb,
	'jc': ccf_jc
}

def dblp_json(data):
	papers = []
	text = json.loads(data)
	for i in text['result']['hits']['hit']:
		temp = i['info']
		title = temp['title']
		year = temp['year']
		paper_type = 'c' if 'Conference' in temp['type'] else 'j'
		venue = temp['venue'] if 'venue' in temp else ''
		doi = temp['doi'] if 'doi' in temp else ''

		paper = {
			'type': paper_type,
			'venue': venue,
			'year': year,
			'doi': doi,
			'title': title
		}
		papers.append(paper)
	return papers

# 通过具体刊物进行筛选
def filter_by_venues(papers, paper_type: str) -> List:
	l = []

	for p in papers:
		for v in ccf[paper_type]['venues']:
			# 文章所在的刊物为所搜寻的刊物并且类型一致（会议/期刊）
			if v == p['venue'] and p['type'] in ccf[paper_type]['type']:
				# 将文章类型具体到ABC分类
				p['type'] = ccf[paper_type]['type']
				l.append(p)

	# 将结果按年排序
	l.sort(key=lambda x: x['year'], reverse=True)

	return l

def filter_by_year(papers, b, e):
	l = []

	for p in papers:
		if b <= int(p['year']) <= e:
			l.append(p)
	return l

# 统计得到的文章
def papers_cnt(papers):
	cnt = {}
	rank = ['ca', 'cb', 'cc', 'ja', 'jb', 'jc']
	for t in ccf.keys():
		cnt[t] = 0
	for p in papers:
		cnt[p['type']] += 1

	print('ca=%d\tcb=%d\tcc=%d' % (cnt['ca'], cnt['cb'], cnt['cc']))
	print('ja=%d\tjb=%d\tjc=%d' % (cnt['ja'], cnt['jb'], cnt['jc']))
	c = cnt['ca'] + cnt['cb'] + cnt['cc']
	j = cnt['ja'] + cnt['jb'] + cnt['jc']
	print('Conference : %d\t Journal : %d' % (c, j))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, nargs='?', help='从DBLP获取的搜索结果（JSON格式）')
	parser.add_argument('-k', '--keyword', type=str, nargs='+', help='关键词（不能和目标文件同时指定）')
	parser.add_argument('-r', '--rank', type=str, nargs='+', help='CCF级别: '+ str(tuple(ccf.keys())))
	parser.add_argument('-s', '--startdate', type=int, nargs='?', help='发表时间限制（起点）')
	parser.add_argument('-e', '--enddate', type=int, nargs='?', help='发表时间限制（终点）')
	parser.add_argument('-o', '--outfile', type=str, nargs='?', help='指定输出文件的文件名')
	args = parser.parse_args()

	# 指定了目标文件，从文件中获取数据
	if args.file:
		assert not args.keyword, '不能同时指定目标文件和关键词'
		with open(args.file, 'r', encoding='utf-8') as f:
			data = f.read()
			out_file = args.file.split('.')[0]
	else:
		# 指定了关键字，从dblp数据库获取数据
		if args.keyword:
			url = 'https://dblp.uni-trier.de/search/publ/api?q=' + '%20'.join(args.keyword) + '&h=1000&format=json'
			out_file = '_'.join(args.keyword)
			print('正在请求dblp，关键字："%s"' % out_file)
			print('url: ' + url)
			data = requests.get(url).text
		else:
			assert False, '目标文件和关键字均未指定'

	# 解析数据
	papers = dblp_json(data)

	# 指定文章类型（默认为最大范围）
	if args.rank:
		search_scale = args.rank
	else:
		search_scale = ccf

	temp = []
	for paper_type in search_scale:
		assert paper_type in ccf, '不支持的文章类型：' + paper_type
		temp += filter_by_venues(papers, paper_type)
	papers = temp

	# 指定文章时间
	begin_year = args.startdate or 0
	end_year = args.enddate or datetime.now().year
	papers = filter_by_year(papers, begin_year, end_year)

	papers_cnt(papers)

	labels = ['type', 'venue', 'year', 'doi', 'title']
	if args.outfile:
		out_file = args.outfile
	else:
		out_file += '_' + 'result.csv'
	with open(out_file, 'w') as f:
		writer = csv.DictWriter(f, fieldnames=labels, lineterminator='\n')
		writer.writeheader()
		for elem in papers:
			writer.writerow(elem)
	print('结果保存在文件：' + out_file)
