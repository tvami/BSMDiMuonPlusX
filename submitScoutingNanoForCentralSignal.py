import sys, os, time, re
from threading import Thread

datasetList = []
dataset_TpTpTo2T2STo2Mu2G = [
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS100_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS15_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS25_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS30_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS35_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS40_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS45_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS50_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS55_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS60_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS65_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS70_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS75_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS80_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS85_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS90_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2G_Par-MTp1000-MS95_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS100_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS25_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS30_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS35_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS40_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS45_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS50_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS55_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS60_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS65_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS70_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS75_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS80_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS90_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2MuInv_Par-MTp1000-MS95_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
]

dataset_TpTpTo2T2STo2Mu2B = [
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS10_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS15_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS20_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS25_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS30_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS35_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS40_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS45_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS50_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS55_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS60_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS65_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS70_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS75_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS80_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS85_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS90_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS95_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
	"/TpTpTo2T2STo2Mu2B_Par-MTp1000-MS100_TuneCP5_13p6TeV_madgraph-pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM",
]

# add TpTpTo2T2STo2Mu2G to datasetList
# datasetList.extend(dataset_TpTpTo2T2STo2Mu2G)
# add TpTpTo2T2STo2Mu2B to datasetList
datasetList.extend(dataset_TpTpTo2T2STo2Mu2B)

if not os.path.exists("submittedConfigs"): os.makedirs("submittedConfigs")

if not os.path.exists("4crab_Signal_TemplateMT.py"):
  TEMPLATE = '''
from CRABClient.UserUtilities import config
config = config()

config.section_('General')
config.General.requestName = 'ROVIDMINTA_NanoAODScoutingFlat_2024_v2'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'NanoAODScouting-01654_1_flat_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.outputFiles = ['Summer24NanoAODv15-01654_scouting_flat.root']


config.section_('Data')
config.Data.inputDataset = 'MINTA'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outputDatasetTag = config.General.requestName
config.Data.outLFNDirBase = '/store/user/tvami/DiMuonPlusX'
config.Data.ignoreLocality = True
config.Data.partialDataset = True
config.Data.publication = True 

config.section_('Site')
config.Site.whitelist = ['T2_DE_DESY','T2_CH_CERN','T2_IT_Bari','T1_IT_*','T2_US_*', 'T3_US_FNALLPC','T2_HU_Budapest','T2_FR_*', 'T2_UK_London_IC']
config.Site.storageSite = 'T2_US_UCSD'
  '''

  with open("4crab_Signal_TemplateMT.py", "w") as text_file:
      text_file.write(TEMPLATE)

def task(i):
  #print("Submit for sample "+i)
  os.system("cp 4crab_Signal_TemplateMT.py 4crab_Signal_toSubmit"+str(i.replace("/","_"))+".py")
  shortSampleName = i[1:(i.find('TuneCP5'))-1]
  replaceROVIDMINTA = "sed -i 's/ROVIDMINTA/"+shortSampleName+"/g' 4crab_Signal_toSubmit"+str(i.replace("/","_"))+".py"
  os.system(replaceROVIDMINTA)
  replaceMINTA = "sed -i 's/MINTA/"+i.replace("/","\/")+"/g' 4crab_Signal_toSubmit"+str(i.replace("/","_"))+".py"
  os.system(replaceMINTA)
  os.system("crab submit -c 4crab_Signal_toSubmit"+str(i.replace("/","_"))+".py")
  os.system("mv 4crab_Signal_toSubmit"+str(i.replace("/","_"))+".py submittedConfigs/.")
  
threads = []
for dataset in datasetList:
  t = Thread(target=task, args=(dataset,))
  threads.append(t)
  t.start()

for t in threads:
    t.join()



os.system("rm 4crab_Signal_TemplateMT.py")

