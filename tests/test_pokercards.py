#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2006 - 2010 Loic Dachary <loic@dachary.org>
# Copyright (C) 2006 Mekensleep
#
# Mekensleep
# 26 rue des rosiers
# 75004 Paris
#       licensing@mekensleep.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Authors:
#  Pierre-Andre (05/2006)
#  Loic Dachary <loic@dachary.org>
#

import unittest, sys
from os import path

TESTS_PATH = path.dirname(path.realpath(__file__))
sys.path.insert(0, path.join(TESTS_PATH, ".."))

from pokerengine import pokercards


class PokerCardsTestCase(unittest.TestCase):
    
    # -----------------------------------------------------------------------------------------------------
    def setUp(self):
        pass
    
    # -----------------------------------------------------------------------------------------------------    
    def tearDown(self):
        pass
        
    # -----------------------------------------------------------------------------------------------------    
    def testInit(self):
        """Test PokerCards : Creation of cards"""
        
        empty = pokercards.PokerCards()
        self.failUnlessEqual(empty.toRawList(), [])
        
        cards = pokercards.PokerCards(12)
        self.failUnlessEqual(cards.toRawList(), [12])
        self.failUnless(cards.areVisible())
        
        cards = pokercards.PokerCards([12, 25, 37, pokercards.PokerCards.NOCARD])
        self.failUnlessEqual(cards.toRawList(), [12, 25, 37, pokercards.PokerCards.NOCARD])
        self.failIf(cards.areVisible())
        
        cards = pokercards.PokerCards('Ah')
        self.failUnlessEqual(cards.toRawList(), [12])
        self.failUnless(cards.areVisible())
        
        cards = pokercards.PokerCards(['Ah', 'Ad', 'Kc'])
        self.failUnlessEqual(cards.toRawList(), [12, 25, 37])
        self.failUnless(cards.areVisible())
        
        cards = pokercards.PokerCards(['Ah', 25, 'Kc'])
        self.failUnlessEqual(cards.toRawList(), [12, 25, 37])
        self.failUnless(cards.areVisible())
        
        cards2 = pokercards.PokerCards(cards)
        self.failUnlessEqual(cards2, cards)
        
    # -----------------------------------------------------------------------------------------------------    
    def TestGetValue(self):
        """Test PokerCards : Get value"""
        
        cards = pokercards.PokerCards()
        self.failUnlessEqual(cards.getValue(12), 12)
        self.failUnlessEqual(cards.getValue('Ah'), 12)
        self.failUnlessEqual(cards.getValue(pokercards.PokerCards.NOCARD), 255)
        self.failUnlessRaises(UserWarning, cards.add, 52, True)
        self.failUnlessRaises(UserWarning, cards.add, -1, True)
        self.failUnlessRaises(UserWarning, cards.add, 'Aa', True)
        
    # -----------------------------------------------------------------------------------------------------    
    def testAddInvalid(self):
        """Test PokerCards : Invalid card adding"""
        
        cards = pokercards.PokerCards()
        self.failUnlessRaises(UserWarning,cards.add, 52, True)
        self.failUnlessRaises(UserWarning,cards.add, -1, True)
        self.failUnlessRaises(UserWarning,cards.add, 'Aa', True)
                
    # -----------------------------------------------------------------------------------------------------    
    def testAddVisible(self):
        """Test PokerCards : Add visible card"""
        
        cards = pokercards.PokerCards()
        cards.add(12, True)
        self.failUnless(cards.hasCard(12))
        self.failUnlessEqual(cards.getVisible(), [12])
        
        cards = pokercards.PokerCards()
        cards.add('3s', True)
        self.failUnless(cards.hasCard(40))
        self.failUnlessEqual(cards.getVisible(), [40])
        
        cards.add(cards.nocard(), True)
        self.failUnless(cards.hasCard(cards.nocard()))
        
    # -----------------------------------------------------------------------------------------------------    
    def testAddInvisible(self):
        """Test PokerCards : Add invisible card"""
        
        cards = pokercards.PokerCards()
        cards.add(12, False)
        self.failUnless(cards.hasCard(12))        
        self.failUnlessEqual(cards.getVisible(), [])
        
        cards = pokercards.PokerCards()
        cards.add('3s', False)
        self.failUnless(cards.hasCard(40))
        self.failUnlessEqual(cards.getVisible(), [])
        
    # -----------------------------------------------------------------------------------------------------    
    def testAllVisible(self):
        """Test PokerCards : All cards visible"""
        
        cards = pokercards.PokerCards()
        cards.add(12, False)
        cards.add(25, False)
        cards.add(45, False)
        
        self.failUnlessEqual(cards.getVisible(), [])
        cards.allVisible()
        self.failUnless(cards.areVisible())
        
    # -----------------------------------------------------------------------------------------------------    
    def testAllHidden(self):
        """Test PokerCards : All cards hidden"""
        
        cards = pokercards.PokerCards()
        cards.add(12, True)
        cards.add(25, False)
        cards.add(45, True)
        
        self.failUnlessEqual(cards.getVisible(), [12, 45])
        self.failIf(cards.areHidden())
        cards.allHidden()
        self.failUnless(cards.areHidden())
        
    # -----------------------------------------------------------------------------------------------------    
    def testSetVisible(self):
        """Test PokerCards : Set card visible"""
        
        cards = pokercards.PokerCards()
        cards.add(12, True)
        self.failUnlessEqual(cards.getVisible(), [12])
        
        cards.setVisible(12,False)
        self.failUnlessEqual(cards.getVisible(), [])
        
        cards.setVisible(12,True)
        self.failUnlessEqual(cards.getVisible(), [12])
        
        cards.setVisible(15,True)
        self.failUnlessEqual(cards.getVisible(), [12])
        
        cards.setVisible(cards.nocard(),False)
        self.failUnlessEqual(cards.getVisible(), [12])
        
    # -----------------------------------------------------------------------------------------------------    
    def testIsEmpty(self):
        """Test PokerCards : Is empty"""
        
        cards = pokercards.PokerCards()
        self.failUnless(cards.isEmpty())
        
        cards.add(12, True)
        self.failIf(cards.isEmpty())
        
    # -----------------------------------------------------------------------------------------------------    
    def testLen(self):
        """Test PokerCards : Cards lenght"""
        
        cards = pokercards.PokerCards()
        self.failUnlessEqual(cards.len(), 0)
        
        cards.add(12, True)
        self.failUnlessEqual(cards.len(), 1)
        
    # -----------------------------------------------------------------------------------------------------    
    def testHasCard(self):
        """Test PokerCards : Has card"""
        
        cards = pokercards.PokerCards([12,26])
        self.failUnless(cards.hasCard(12))
        self.failIf(cards.hasCard(27))
        
    # -----------------------------------------------------------------------------------------------------    
    def testOperatorEqu(self):
        """Test PokerCards : Cards operator equ and ne"""
        
        cards1 = pokercards.PokerCards([12,26])
        cards2 = pokercards.PokerCards([26,12])
        cards3 = pokercards.PokerCards([26,12,50])
        
        self.failIf(cards1 == [12,26])
        self.failUnless(cards1 != [12,26])
        
        self.failUnless(cards1 == cards2)
        self.failIf(cards1 == cards3)
        self.failUnless(cards1 != cards3)
        
    # -----------------------------------------------------------------------------------------------------    
    def testCopy(self):
        """Test PokerCards : Cards copy"""
        
        cards1 = pokercards.PokerCards([12,26])
        cards2 = cards1.copy()
        self.failUnless(cards1 == cards2)
        cards2.add(13,True)
        self.failIf(cards1 == cards2)
        
    # -----------------------------------------------------------------------------------------------------    
    def testToList(self):
        """Test PokerCards : Cards to list"""
        
        cards = pokercards.PokerCards([12,26])
        self.failUnlessEqual(cards.tolist(False), [12,26])
        self.failUnlessEqual(cards.tolist(True), [12,26])
        
        cards.setVisible(26,False)
        self.failUnlessEqual(cards.tolist(False), [12, cards.nocard()])
        self.failUnlessEqual(cards.tolist(True), [12, 26])
        
        cards.allHidden()
        self.failUnlessEqual(cards.tolist(False), [cards.nocard(), cards.nocard()])
        self.failUnlessEqual(cards.tolist(True), [12, 26])
        
    # -----------------------------------------------------------------------------------------------------    
    def testNoCard(self):
        """Test PokerCards : No card value"""
        
        cards = pokercards.PokerCards()
        self.failUnlessEqual(cards.nocard(), pokercards.PokerCards.NOCARD)
        
    # -----------------------------------------------------------------------------------------------------    
    def testAreAllNocard(self):
        """Test PokerCards : Are all no card"""
        
        cards = pokercards.PokerCards([12,26])
        self.failIf(cards.areAllNocard())
        cards = pokercards.PokerCards([cards.nocard(), 26])
        self.failIf(cards.areAllNocard())
        cards = pokercards.PokerCards([cards.nocard(), cards.nocard()])
        self.failUnless(cards.areAllNocard())
        
    # -----------------------------------------------------------------------------------------------------    
    def testLoseNotVisible(self):
        """Test PokerCards : Lose not visible"""
        
        cards = pokercards.PokerCards([12,26])
        cards.loseNotVisible()
        self.failUnlessEqual(cards.toRawList(), [12,26])
        cards.add(33, False)
        cards.loseNotVisible()
        self.failUnlessEqual(cards.toRawList(), [12,26,cards.nocard()])
        cards.add(43, True)
        cards.loseNotVisible()
        self.failUnlessEqual(cards.toRawList(), [12,26,cards.nocard(),43])
        cards.add(cards.nocard(), True)
        cards.loseNotVisible()
        self.failUnlessEqual(cards.toRawList(), [12,26,cards.nocard(),43, cards.nocard()])
        
    # -----------------------------------------------------------------------------------------------------    
    def testOperatorRepr(self):
        """Test PokerCards : Operator repr"""
        
        cards = pokercards.PokerCards([12,26])
        self.failUnlessEqual(repr(cards), '%s(%s)' %('PokerCards', [12,26]))
        
    # -----------------------------------------------------------------------------------------------------    
    def testOperatorStr(self):
        """Test PokerCards : Operator str"""
        
        cards = pokercards.PokerCards()
        cards.add(12, True)
        cards.add(26, False)
        self.failUnlessEqual(str(cards), str([ 'Card(12, visible)', 'Card(26, not visible)']))
        
# -----------------------------------------------------------------------------------------------------
def GetTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PokerCardsTestCase))
    # Comment out above and use line below this when you wish to run just
    # one test by itself (changing prefix as needed).
#    suite.addTest(unittest.makeSuite(PokerCardsTestCase, prefix = "test2"))
    return suite
    
# -----------------------------------------------------------------------------------------------------
def GetTestedModule():
    return pokercards
  
# -----------------------------------------------------------------------------------------------------
def run():
    return unittest.TextTestRunner().run(GetTestSuite())
    
# -----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    if run().wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
