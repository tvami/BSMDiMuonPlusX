import os
import glob

from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'TpTpTo2T2STo2Mu2G-mT-1000-mS-100_AOD_2024_v1'

config.section_('JobType')
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'EXO-RunIII2024Summer24DRPremix-01654_2_cfg.py'
config.JobType.outputFiles = ['EXO-RunIII2024Summer24DRPremix-01654.root']
config.JobType.disableAutomaticOutputCollection = True
config.JobType.maxMemoryMB = 4500
#config.JobType.numCores = 8

config.section_('Data')
config.Data.inputDBS = 'phys03'
config.Data.inputDataset = '/TpTpTo2T2STo2Mu2G-mT-1000-mS-100_GENSIM_2024_v1_13p6TeV/tvami-crab_TpTpTo2T2STo2Mu2G-mT-1000-mS-100_DR_2024_v1-e5438bb52f42c4163dc01d5bb2e896e9/USER'
config.Data.outLFNDirBase = '/store/user/tvami/DiMuonPlusX/'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.ignoreLocality = True
config.Data.publication = True

config.section_('Site')
config.Site.storageSite = 'T2_US_UCSD'
config.Site.whitelist = ['T2_DE_DESY','T2_CH_CERN','T2_IT_Bari','T1_IT_*','T2_US_*', 'T3_US_FNALLPC','T2_HU_Budapest','T2_FR_*', 'T2_UK_London_IC']
