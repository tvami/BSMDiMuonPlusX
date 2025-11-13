import os
import glob

from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'TpTpTo2T2STo2Mu2G-mT-1000-mS-100_MiniAOD_2024_v1'

config.section_('JobType')
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'EXO-RunIII2024Summer24MiniAODv6-01654_1_cfg.py'
config.JobType.outputFiles = ['EXO-RunIII2024Summer24MiniAODv6-01654.root']
config.JobType.disableAutomaticOutputCollection = True
config.JobType.maxMemoryMB = 4000
#config.JobType.numCores = 8

config.section_('Data')
config.Data.inputDBS = 'phys03'
config.Data.inputDataset = '/TpTpTo2T2STo2Mu2G-mT-1000-mS-100_GENSIM_2024_v1_13p6TeV/tvami-crab_TpTpTo2T2STo2Mu2G-mT-1000-mS-100_AOD_2024_v1-89578c67bc58e175e14cb8efc9d9e047/USER'
config.Data.outLFNDirBase = '/store/user/tvami/DiMuonPlusX/'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.ignoreLocality = True
config.Data.publication = True

config.section_('Site')
config.Site.storageSite = 'T2_US_UCSD'
config.Site.whitelist = ['T2_DE_DESY','T2_CH_CERN','T2_IT_Bari','T1_IT_*','T2_US_*', 'T3_US_FNALLPC','T2_HU_Budapest','T2_FR_*', 'T2_UK_London_IC']
