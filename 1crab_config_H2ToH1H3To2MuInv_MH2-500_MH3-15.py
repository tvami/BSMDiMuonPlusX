import os
import glob

from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'H2ToH1H3To2MuInv_MH2-500_MH3-15_GENSIM_2024_v1_13p6TeV'

config.section_('JobType')
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'H2ToH1H3To2MuInv_MH2-500_MH3-15_GENSIM_cfg.py'
config.JobType.inputFiles = []
config.JobType.outputFiles = ['GENSIM.root']
config.JobType.disableAutomaticOutputCollection = True
# config.JobType.maxMemoryMB = 3500

config.section_('Data')
config.Data.outLFNDirBase = '/store/user/tvami/DiMuonPlusX/'
config.Data.outputPrimaryDataset = config.General.requestName
config.Data.outputDatasetTag = config.General.requestName
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 200
config.Data.totalUnits = 200000
config.Data.ignoreLocality = True
config.Data.publication = True

config.section_('Site')
config.Site.storageSite = 'T2_US_UCSD'
config.Site.whitelist = ['T2_DE_DESY','T2_CH_CERN','T2_IT_Bari','T1_IT_*','T2_US_*', 'T3_US_FNALLPC','T2_HU_Budapest','T2_FR_*', 'T2_UK_London_IC']
