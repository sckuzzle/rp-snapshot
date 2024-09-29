# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 19:03:03 2023

script for creating historical staking snapshots for Rocket Pool

@author: sckuzzle

contains components used from a staking snapshot creation tool by Valdorff at 
https://github.com/Valdorff/rp-thoughts/blob/main/rpl_staking/get_staking_snapshot_2.py
"""

import time
import os
import requests
import json

from web3 import Web3, HTTPProvider
import pandas as pd

LATEST_INTERVAL = 27

def get_network_df():
  df = pd.read_csv('staking_snapshot.csv')
  return df

def get_index():
  df = pd.read_csv('./snapshot/index.csv')
  return df

def create_snapshots_at_interval():
  """wrapper to loop through and create a staking snapshot at each interval point specified"""
  RocketStorage, RocketNodeManager, RocketNodeStaking, RocketNetworkPrices, RocketTokenRPL, RocketRewardsPool, RocketRETH, wETH = get_contracts('latest')
  for interval in range(27, LATEST_INTERVAL+1):
    block_id = RocketRewardsPool.functions.getClaimIntervalExecutionBlock(interval).call()
    print(f'{interval=} {block_id=}')
    create_snapshot(block_id)

def create_index():
  
  RocketStorage, RocketNodeManager, RocketNodeStaking, RocketNetworkPrices, RocketTokenRPL, RocketRewardsPool, RocketRETH, wETH = get_contracts('latest')
  block_id = RocketRewardsPool.functions.getClaimIntervalExecutionBlock(LATEST_INTERVAL).call()
  RocketStorage, RocketNodeManager, RocketNodeStaking, RocketNetworkPrices, RocketTokenRPL, RocketRewardsPool, RocketRETH, wETH = get_contracts(block_id)
  num_nodes = RocketNodeManager.functions.getNodeCount().call(block_identifier = block_id)
  addr_ls = []
  with_addr_ls = []
  
  for offset in range(0, num_nodes, 100):
    node_ls = RocketNodeManager.functions.getNodeAddresses(offset, 100).call(block_identifier = block_id)
    
    for addr in node_ls:
        with_addr = RocketStorage.functions.getNodeWithdrawalAddress(addr).call(block_identifier = block_id)
        addr_ls.append(addr)
        with_addr_ls.append(with_addr)
        
  df = pd.DataFrame({
      'address': addr_ls,
      'withdrawal_address': with_addr_ls,
  })
  
  df.to_csv(f'./snapshot/index.csv')
  
  
def get_contracts(block_id = 'latest'):
  """Finds the address for each contract, fetches the abi for that contract, and returns web3 contract objects at the given block_id"""

  if block_id =='latest':  
    NODE_IP = os.environ['node_ip']
    
    CLIENT = Web3(Web3.HTTPProvider(f'http://{NODE_IP}:8545'))
  else:
    ARCHIVE_NODE_IP = os.environ['archive_node_ip']
    
    CLIENT = Web3(Web3.HTTPProvider(f'{ARCHIVE_NODE_IP}'))
  API_KEY = os.environ['api_key']
  
  
  RocketStorage = CLIENT.eth.contract(
      address=Web3.toChecksumAddress("0x1d8f8f00cfa6758d7bE78336684788Fb0ee0Fa46"),
      abi=
      '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"oldGuardian","type":"address"},{"indexed":false,"internalType":"address","name":"newGuardian","type":"address"}],"name":"GuardianChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"node","type":"address"},{"indexed":true,"internalType":"address","name":"withdrawalAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"time","type":"uint256"}],"name":"NodeWithdrawalAddressSet","type":"event"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"addUint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"confirmGuardian","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"}],"name":"confirmWithdrawalAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"}],"name":"deleteAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"}],"name":"deleteBool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"}],"name":"deleteBytes","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"}],"name":"deleteBytes32","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"}],"name":"deleteInt","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"}],"name":"deleteString","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"}],"name":"deleteUint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"}],"name":"getAddress","outputs":[{"internalType":"address","name":"r","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"}],"name":"getBool","outputs":[{"internalType":"bool","name":"r","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"}],"name":"getBytes","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"}],"name":"getBytes32","outputs":[{"internalType":"bytes32","name":"r","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getDeployedStatus","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getGuardian","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"}],"name":"getInt","outputs":[{"internalType":"int256","name":"r","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"}],"name":"getNodePendingWithdrawalAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"}],"name":"getNodeWithdrawalAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"}],"name":"getString","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"}],"name":"getUint","outputs":[{"internalType":"uint256","name":"r","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"},{"internalType":"address","name":"_value","type":"address"}],"name":"setAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"},{"internalType":"bool","name":"_value","type":"bool"}],"name":"setBool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"},{"internalType":"bytes","name":"_value","type":"bytes"}],"name":"setBytes","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"},{"internalType":"bytes32","name":"_value","type":"bytes32"}],"name":"setBytes32","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"setDeployedStatus","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_newAddress","type":"address"}],"name":"setGuardian","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"},{"internalType":"int256","name":"_value","type":"int256"}],"name":"setInt","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"},{"internalType":"string","name":"_value","type":"string"}],"name":"setString","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"setUint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"},{"internalType":"address","name":"_newWithdrawalAddress","type":"address"},{"internalType":"bool","name":"_confirm","type":"bool"}],"name":"setWithdrawalAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_key","type":"bytes32"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"subUint","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
  )
  
  manager_address = address = RocketStorage.functions.getAddress(Web3.solidityKeccak(['string', 'string'], ["contract.address", "rocketNodeManager"])).call(block_identifier = block_id)
  abi = requests.get(f"https://api.etherscan.io/api?module=contract&action=getabi&address={manager_address}&apikey={API_KEY}")
  
  # json_dict = json.loads(abi)
  RocketNodeManager = CLIENT.eth.contract(
      address=Web3.toChecksumAddress(manager_address),
      abi=
      '[{"inputs":[{"internalType":"contract RocketStorageInterface","name":"_rocketStorageAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"node","type":"address"},{"indexed":false,"internalType":"uint256","name":"time","type":"uint256"}],"name":"NodeRegistered","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"node","type":"address"},{"indexed":false,"internalType":"uint256","name":"network","type":"uint256"}],"name":"NodeRewardNetworkChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"node","type":"address"},{"indexed":false,"internalType":"bool","name":"state","type":"bool"}],"name":"NodeSmoothingPoolStateChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"node","type":"address"},{"indexed":false,"internalType":"uint256","name":"time","type":"uint256"}],"name":"NodeTimezoneLocationSet","type":"event"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"}],"name":"getAverageNodeFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"}],"name":"getFeeDistributorInitialised","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_offset","type":"uint256"},{"internalType":"uint256","name":"_limit","type":"uint256"}],"name":"getNodeAddresses","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"getNodeAt","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getNodeCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_offset","type":"uint256"},{"internalType":"uint256","name":"_limit","type":"uint256"}],"name":"getNodeCountPerTimezone","outputs":[{"components":[{"internalType":"string","name":"timezone","type":"string"},{"internalType":"uint256","name":"count","type":"uint256"}],"internalType":"struct RocketNodeManagerInterface.TimezoneCount[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"}],"name":"getNodeDetails","outputs":[{"components":[{"internalType":"bool","name":"exists","type":"bool"},{"internalType":"uint256","name":"registrationTime","type":"uint256"},{"internalType":"string","name":"timezoneLocation","type":"string"},{"internalType":"bool","name":"feeDistributorInitialised","type":"bool"},{"internalType":"address","name":"feeDistributorAddress","type":"address"},{"internalType":"uint256","name":"rewardNetwork","type":"uint256"},{"internalType":"uint256","name":"rplStake","type":"uint256"},{"internalType":"uint256","name":"effectiveRPLStake","type":"uint256"},{"internalType":"uint256","name":"minimumRPLStake","type":"uint256"},{"internalType":"uint256","name":"maximumRPLStake","type":"uint256"},{"internalType":"uint256","name":"ethMatched","type":"uint256"},{"internalType":"uint256","name":"ethMatchedLimit","type":"uint256"},{"internalType":"uint256","name":"minipoolCount","type":"uint256"},{"internalType":"uint256","name":"balanceETH","type":"uint256"},{"internalType":"uint256","name":"balanceRETH","type":"uint256"},{"internalType":"uint256","name":"balanceRPL","type":"uint256"},{"internalType":"uint256","name":"balanceOldRPL","type":"uint256"},{"internalType":"uint256","name":"depositCreditBalance","type":"uint256"},{"internalType":"uint256","name":"distributorBalanceUserETH","type":"uint256"},{"internalType":"uint256","name":"distributorBalanceNodeETH","type":"uint256"},{"internalType":"address","name":"withdrawalAddress","type":"address"},{"internalType":"address","name":"pendingWithdrawalAddress","type":"address"},{"internalType":"bool","name":"smoothingPoolRegistrationState","type":"bool"},{"internalType":"uint256","name":"smoothingPoolRegistrationChanged","type":"uint256"},{"internalType":"address","name":"nodeAddress","type":"address"}],"internalType":"struct NodeDetails","name":"nodeDetails","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"}],"name":"getNodeExists","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"}],"name":"getNodePendingWithdrawalAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"}],"name":"getNodeRegistrationTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"}],"name":"getNodeTimezoneLocation","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"}],"name":"getNodeWithdrawalAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"}],"name":"getRewardNetwork","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_offset","type":"uint256"},{"internalType":"uint256","name":"_limit","type":"uint256"}],"name":"getSmoothingPoolRegisteredNodeCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"}],"name":"getSmoothingPoolRegistrationChanged","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"}],"name":"getSmoothingPoolRegistrationState","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"initialiseFeeDistributor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_timezoneLocation","type":"string"}],"name":"registerNode","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_nodeAddress","type":"address"},{"internalType":"uint256","name":"_network","type":"uint256"}],"name":"setRewardNetwork","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_state","type":"bool"}],"name":"setSmoothingPoolRegistrationState","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_timezoneLocation","type":"string"}],"name":"setTimezoneLocation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'
  )
  
  staking_address = address = RocketStorage.functions.getAddress(Web3.solidityKeccak(['string', 'string'], ["contract.address", "rocketNodeStaking"])).call(block_identifier = block_id)
  abi = requests.get(f"https://api.etherscan.io/api?module=contract&action=getabi&address={staking_address}&apikey={API_KEY}")
  RocketNodeStaking = CLIENT.eth.contract(
      address=Web3.toChecksumAddress(staking_address),
      abi=abi.json()['result']
  )
  
  prices_address = address = RocketStorage.functions.getAddress(Web3.solidityKeccak(['string', 'string'], ["contract.address", "rocketNetworkPrices"])).call(block_identifier = block_id)
  abi = requests.get(f"https://api.etherscan.io/api?module=contract&action=getabi&address={prices_address}&apikey={API_KEY}")
  RocketNetworkPrices = CLIENT.eth.contract(
      address=Web3.toChecksumAddress(prices_address),
      abi=abi.json()['result']
  )
  
  time.sleep(1.5)
  rpl_address = address = RocketStorage.functions.getAddress(Web3.solidityKeccak(['string', 'string'], ["contract.address", "rocketTokenRPL"])).call(block_identifier = block_id)
  abi = requests.get(f"https://api.etherscan.io/api?module=contract&action=getabi&address={rpl_address}&apikey={API_KEY}")
  RocketTokenRPL = CLIENT.eth.contract(
      address=Web3.toChecksumAddress(rpl_address),
      abi=abi.json()['result']
  )
  
  rewards_address = address = RocketStorage.functions.getAddress(Web3.solidityKeccak(['string', 'string'], ["contract.address", "rocketRewardsPool"])).call(block_identifier = block_id)
  abi = requests.get(f"https://api.etherscan.io/api?module=contract&action=getabi&address={rewards_address}&apikey={API_KEY}")
  RocketRewardsPool = CLIENT.eth.contract(
      address=Web3.toChecksumAddress(rewards_address),
      abi=abi.json()['result']
  )
  
  RETH_address = address = RocketStorage.functions.getAddress(Web3.solidityKeccak(['string', 'string'], ["contract.address", "rocketTokenRETH"])).call(block_identifier = block_id)
  abi = requests.get(f"https://api.etherscan.io/api?module=contract&action=getabi&address={RETH_address}&apikey={API_KEY}")
  RocketRETH = CLIENT.eth.contract(
      address=Web3.toChecksumAddress(RETH_address),
      abi=abi.json()['result']
  )
  
  wETH = CLIENT.eth.contract(
      address=Web3.toChecksumAddress("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"),
      abi=abi.json()['result']
  )
  return RocketStorage, RocketNodeManager, RocketNodeStaking, RocketNetworkPrices, RocketTokenRPL, RocketRewardsPool, RocketRETH, wETH

def create_snapshot(block):
  """Creates a snapshots at the given block and saves it at {block}.csv"""
  RocketStorage, RocketNodeManager, RocketNodeStaking, RocketNetworkPrices, RocketTokenRPL, RocketRewardsPool, RocketRETH, wETH = get_contracts(block)
  
  
  num_nodes = RocketNodeManager.functions.getNodeCount().call(block_identifier = block)
  
  rpl_price_in_eth = RocketNetworkPrices.functions.getRPLPrice().call() / 1e18
  addr_ls = []
  with_addr_ls = []
  provided_eth_ls = []
  matched_eth_ls = []
  staked_rpl_ls = []
  liquid_rpl_node_ls = []
  liquid_rpl_with_ls = []
  
  for offset in range(0, num_nodes, 100):
      print(offset)
      node_ls = RocketNodeManager.functions.getNodeAddresses(offset, 100).call(block_identifier = block)
      for addr in node_ls:
          with_addr = RocketStorage.functions.getNodeWithdrawalAddress(addr).call(block_identifier = block)
  
          addr_ls.append(addr)
          with_addr_ls.append(with_addr)
          provided_eth_ls.append(RocketNodeStaking.functions.getNodeETHProvided(addr).call(block_identifier = block))
          matched_eth_ls.append(RocketNodeStaking.functions.getNodeETHMatched(addr).call(block_identifier = block))
          rpl_stake = RocketNodeStaking.functions.getNodeRPLStake(addr).call(block_identifier = block)
          rpl_node = RocketTokenRPL.functions.balanceOf(addr).call(block_identifier = block)
          rpl_with = RocketTokenRPL.functions.balanceOf(with_addr).call(block_identifier = block)
          staked_rpl_ls.append(rpl_stake)
          liquid_rpl_node_ls.append(rpl_node)
          liquid_rpl_with_ls.append(rpl_with)
  
  df = pd.DataFrame({
      'address': addr_ls,
      'withdrawal_address': with_addr_ls,
      'staked_RPL': staked_rpl_ls,
      'node_RPL':  liquid_rpl_node_ls,
      'withdrawal_RPL': liquid_rpl_with_ls, 
      'nETH': provided_eth_ls,
      'pETH': matched_eth_ls,


  })
  df['staked_RPL'] /= 1e18
  df['nETH'] /= 1e18
  df['pETH'] /= 1e18
  df['node_RPL'] /= 1e18
  df['withdrawal_RPL'] /= 1e18
  df.to_csv(f'./snapshot/{block}.csv')
  
def create_prices():
  """Gathers RPL ratio at the beginning of each interval and saves it to a csv"""
  prices = {}
  RocketStorage, RocketNodeManager, RocketNodeStaking, RocketNetworkPrices, RocketTokenRPL, RocketRewardsPool, RocketRETH, wETH = get_contracts('latest')
  for interval in range(0, 28):
    print(f'{interval=}')
    block_id = RocketRewardsPool.functions.getClaimIntervalExecutionBlock(interval).call()
    time.sleep(1.5)
    _, _, _, RocketNetworkPrices,_, _, _, _ = get_contracts(block_id)
    rpl_price = RocketNetworkPrices.functions.getRPLPrice().call(block_identifier = block_id) / 1e18
    prices[block_id] = rpl_price
  prices = pd.DataFrame.from_dict(prices, orient = 'index', columns = ['ratio'])
  prices.to_csv(f'./snapshot/prices.csv')
  return prices



if __name__=='__main__':

  
  
  # create_index()
  create_snapshots_at_interval()
  # df = create_prices()