#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012-2013 Inria. All rights reserved.
# Author: Stéphane Glondu <Stephane.Glondu@inria.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Disclaimer: no guarantee on the randomness quality here...
from random import randint

digits = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
token_length = 14

def generate_raw_token():
    res = ""
    number = 0
    for i in range(token_length):
        digit = randint(0, 57)
        number = number * 58 + digit
        res += digits[digit]
    return res, number

def generate_token():
    value, number = generate_raw_token()
    checksum = 53 - (number % 53)
    return (value + digits[checksum])

print(generate_token())
