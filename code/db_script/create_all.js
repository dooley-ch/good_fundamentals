// *******************************************************************************************
//  File:  create_dev.js
//
//  Created: 13-06-2022
//
//  Copyright (c) 2022 James Dooley <james@dooley.ch>
//
//  History:
//  13-06-2022: Initial version
//
// *******************************************************************************************

load("create.js")

const array = ["good_fundamentals_prod", "good_fundamentals_test", "good_fundamentals_dev"]

array.forEach(function (item, index) {
  create_database(item);
});
