// *******************************************************************************************
//  File:  create.js
//
//  Created: 13-06-2022
//
//  Copyright (c) 2022 James Dooley <james@dooley.ch>
//
//  History:
//  13-06-2022: Initial version
//
// *******************************************************************************************
// noinspection JSUnresolvedFunction,JSUnresolvedVariable

function create_master(db) {
    db.createCollection('master', {
      validator: {
        $jsonSchema: {
          bsonType: 'object',
          title: 'master',
          required: ['ticker', 'name', 'cik', 'figi', 'sub_industry', 'indexes', 'metadata'],
          properties: {
            ticker: {
              bsonType: 'string'
            },
            name: {
              bsonType: 'string'
            },
            cik: {
              bsonType: 'string'
            },
            figi: {
              bsonType: 'string'
            },
            sub_industry: {
              bsonType: 'string'
            },
            indexes: {
              bsonType: 'array',
              items: {
                bsonType: 'string'
              }
            },
            metadata: {
              bsonType: 'object',
              title: 'metadata',
              required: ['lock_version', 'created_at', 'updated_at'],
              properties: {
                lock_version: {
                  bsonType: 'int'
                },
                created_at: {
                  bsonType: 'date'
                },
                updated_at: {
                  bsonType: 'date'
                }
              }
            }
          }
        }
      }
    });
    db.master.createIndex({
      "ticker": 1
    }, {
      name: "company_ix_ticker",
      unique: true
    })

    db.master.createIndex({
      "cik": 1
    }, {
      name: "master_ix_cik"
    })

    db.master.createIndex({
      "figi": 1
    }, {
      name: "master_ix_figi"
    })

    db.master.createIndex({
      "ticker": 1,
      "name": 1,
      "cik": 1,
      "figi": 1,
      "sub_industry": 1
    }, {
      name: "master_ix_ticker_search"
    })

    db.master.createIndex({
      "name": 1,
      "ticker": 1,
      "cik": 1,
      "figi": 1,
      "sub_industry": 1
    }, {
      name: "master_ix_name_search"
    });
}

function create_gics_sector(db) {
    db.createCollection('gics_sector', {
      validator: {
        $jsonSchema: {
          bsonType: 'object',
          title: 'gics_sector',
          required: ['id', 'name', 'group_industries', 'metadata'],
          properties: {
            id: {
              bsonType: 'int'
            },
            name: {
              bsonType: 'string'
            },
            group_industries: {
              bsonType: 'array',
              items: {
                title: 'group_industry',
                required: ['id', 'name', 'industries'],
                properties: {
                  id: {
                    bsonType: 'int'
                  },
                  name: {
                    bsonType: 'string'
                  },
                  industries: {
                    bsonType: 'array',
                    items: {
                      title: 'gcis_industry',
                      required: ['id', 'name', 'sub_industries'],
                      properties: {
                        id: {
                          bsonType: 'int'
                        },
                        name: {
                          bsonType: 'string'
                        },
                        sub_industries: {
                          bsonType: 'array',
                          items: {
                            title: 'gics_item',
                            required: ['id', 'name'],
                            properties: {
                              id: {
                                bsonType: 'int'
                              },
                              name: {
                                bsonType: 'string'
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            },
            metadata: {
              bsonType: 'object',
              title: 'metadata',
              required: ['lock_version', 'created_at', 'updated_at'],
              properties: {
                lock_version: {
                  bsonType: 'int'
                },
                created_at: {
                  bsonType: 'date'
                },
                updated_at: {
                  bsonType: 'date'
                }
              }
            }
          }
        }
      }
    });
    db.gics_sector.createIndex({
      "name": 1
    }, {
      name: "gics_sector_ix_name",
      unique: true
    })

    db.gics_sector.createIndex({
      "group_industries.name": 1
    }, {
      name: "gics_sector_ix_group_industry_name"
    })

    db.gics_sector.createIndex({
      "group_industries.industries.name": 1
    }, {
      name: "gics_sector_ix_industry_name"
    })

    db.gics_sector.createIndex({
      "group_industries.industries.sub_industries.name": 1
    }, {
      name: "gics_sector_ix_sub_industry_name"
    });
}

function create_company(db) {
    db.createCollection('company', {
        validator: {
            $jsonSchema: {
                bsonType: 'object',
                title: 'company',
                required: ['ticker', 'name', 'description', 'cik', 'figi', 'exchange', 'currency', 'country', 'sub_industry', 'metadata'],
                properties: {
                    ticker: {
                        bsonType: 'string'
                    },
                    name: {
                        bsonType: 'string'
                    },
                    description: {
                        bsonType: 'string'
                    },
                    cik: {
                        bsonType: 'string'
                    },
                    figi: {
                        bsonType: 'string'
                    },
                    exchange: {
                        bsonType: 'string'
                    },
                    currency: {
                        bsonType: 'string'
                    },
                    country: {
                        bsonType: 'string'
                    },
                    sub_industry: {
                        bsonType: 'string'
                    },
                    fiscal_year_end: {
                        bsonType: 'string'
                    },
                    last_quarter: {
                        bsonType: 'date'
                    },
                    metadata: {
                        bsonType: 'object',
                        title: 'metadata',
                        required: ['lock_version', 'created_at', 'updated_at'],
                        properties: {
                            lock_version: {
                                bsonType: 'int'
                            },
                            created_at: {
                                bsonType: 'date'
                            },
                            updated_at: {
                                bsonType: 'date'
                            }
                        }
                    }
                }
            }
        }
    });
    db.company.createIndex({
        "ticker": 1
    }, {
        name: "company_ix_ticker",
        unique: true
    })

    db.company.createIndex({
        "cik": 1
    }, {
        name: "company_ix_cik",
        unique: true
    })

    db.company.createIndex({
        "figi": 1
    }, {
        name: "company_ix_figi",
        unique: true
    });
}

function create_income_statement(db) {
    db.createCollection('income_statement', {
      validator: {
        $jsonSchema: {
          bsonType: 'object',
          title: 'income_statement',
          required: ['period_type', 'ticker', 'items', 'metadata'],
          properties: {
            period_type: {
              enum: ['annual', 'quarter']
            },
            ticker: {
              bsonType: 'string'
            },
            items: {
              bsonType: 'array',
              items: {
                title: 'accounting_entry',
                required: ['tag', 'value_1', 'value_2', 'value_3', 'value_4', 'value_5'],
                properties: {
                  tag: {
                    bsonType: 'string'
                  },
                  value_1: {
                    bsonType: 'string'
                  },
                  value_2: {
                    bsonType: 'string'
                  },
                  value_3: {
                    bsonType: 'string'
                  },
                  value_4: {
                    bsonType: 'string'
                  },
                  value_5: {
                    bsonType: 'string'
                  }
                }
              }
            },
            metadata: {
              bsonType: 'object',
              title: 'metadata',
              required: ['lock_version', 'created_at', 'updated_at'],
              properties: {
                lock_version: {
                  bsonType: 'int'
                },
                created_at: {
                  bsonType: 'date'
                },
                updated_at: {
                  bsonType: 'date'
                }
              }
            }
          }
        }
      }
    });
    db.income_statement.createIndex({
      "ticker": 1,
      "period_type": 1
    }, {
      name: "income_statement_ix_ticker",
      unique: true
    });
}

function create_cash_flow_statement(db) {
    db.createCollection('cash_flow_statement', {
      validator: {
        $jsonSchema: {
          bsonType: 'object',
          title: 'cash_flow_statement',
          required: ['period_type', 'ticker', 'items', 'metadata'],
          properties: {
            period_type: {
              enum: ['annual', 'quarter']
            },
            ticker: {
              bsonType: 'string'
            },
            items: {
              bsonType: 'array',
              items: {
                title: 'accounting_entry',
                required: ['tag', 'value_1', 'value_2', 'value_3', 'value_4', 'value_5'],
                properties: {
                  tag: {
                    bsonType: 'string'
                  },
                  value_1: {
                    bsonType: 'string'
                  },
                  value_2: {
                    bsonType: 'string'
                  },
                  value_3: {
                    bsonType: 'string'
                  },
                  value_4: {
                    bsonType: 'string'
                  },
                  value_5: {
                    bsonType: 'string'
                  }
                }
              }
            },
            metadata: {
              bsonType: 'object',
              title: 'metadata',
              required: ['lock_version', 'created_at', 'updated_at'],
              properties: {
                lock_version: {
                  bsonType: 'int'
                },
                created_at: {
                  bsonType: 'date'
                },
                updated_at: {
                  bsonType: 'date'
                }
              }
            }
          }
        }
      }
    });
    db.cash_flow_statement.createIndex({
      "ticker": 1,
      "period_type": 1
    }, {
      name: "cash_flow_statement_ix_ticker",
      unique: true
    });
}

function create_balance_sheet_statement(db) {
    db.createCollection('balance_sheet_statement', {
      validator: {
        $jsonSchema: {
          bsonType: 'object',
          title: 'balance_sheet_statement',
          required: ['period_type', 'ticker', 'items', 'metadata'],
          properties: {
            period_type: {
              enum: ['annual', 'quarter']
            },
            ticker: {
              bsonType: 'string'
            },
            items: {
              bsonType: 'array',
              items: {
                title: 'accounting_entry',
                required: ['tag', 'value_1', 'value_2', 'value_3', 'value_4', 'value_5'],
                properties: {
                  tag: {
                    bsonType: 'string'
                  },
                  value_1: {
                    bsonType: 'string'
                  },
                  value_2: {
                    bsonType: 'string'
                  },
                  value_3: {
                    bsonType: 'string'
                  },
                  value_4: {
                    bsonType: 'string'
                  },
                  value_5: {
                    bsonType: 'string'
                  }
                }
              }
            },
            metadata: {
              bsonType: 'object',
              title: 'metadata',
              required: ['lock_version', 'created_at', 'updated_at'],
              properties: {
                lock_version: {
                  bsonType: 'int'
                },
                created_at: {
                  bsonType: 'date'
                },
                updated_at: {
                  bsonType: 'date'
                }
              }
            }
          }
        }
      }
    });
    db.balance_sheet_statement.createIndex({
      "ticker": 1,
      "period_type": 1
    }, {
      name: "income_statement_ix_ticker",
      unique: true
    });
}

function create_earnings_statement(db) {
    db.createCollection('earnings_statement', {
      validator: {
        $jsonSchema: {
          bsonType: 'object',
          title: 'earnings_statement',
          required: ['period_type', 'ticker', 'items', 'metadata'],
          properties: {
            period_type: {
              enum: ['annual', 'quarter']
            },
            ticker: {
              bsonType: 'string'
            },
            items: {
              bsonType: 'array',
              items: {
                title: 'accounting_entry',
                required: ['tag', 'value_1', 'value_2', 'value_3', 'value_4', 'value_5'],
                properties: {
                  tag: {
                    bsonType: 'string'
                  },
                  value_1: {
                    bsonType: 'string'
                  },
                  value_2: {
                    bsonType: 'string'
                  },
                  value_3: {
                    bsonType: 'string'
                  },
                  value_4: {
                    bsonType: 'string'
                  },
                  value_5: {
                    bsonType: 'string'
                  }
                }
              }
            },
            metadata: {
              bsonType: 'object',
              title: 'metadata',
              required: ['lock_version', 'created_at', 'updated_at'],
              properties: {
                lock_version: {
                  bsonType: 'int'
                },
                created_at: {
                  bsonType: 'date'
                },
                updated_at: {
                  bsonType: 'date'
                }
              }
            }
          }
        }
      }
    });
    db.earnings_statement.createIndex({
      "ticker": 1,
      "period_type": 1
    }, {
      name: "income_statement_ix_ticker",
      unique: true
    });
}

function create_earnings_file(db) {
    db.createCollection('earnings', {
      validator: {
        $jsonSchema: {
          bsonType: 'object',
          title: 'earnings',
          required: ['ticker', 'name', 'report_date', 'fiscal_year', 'estimate', 'currency', 'metadata'],
          properties: {
            ticker: {
              bsonType: 'string'
            },
            name: {
              bsonType: 'string'
            },
            report_date: {
              bsonType: 'date'
            },
            fiscal_year: {
              bsonType: 'date'
            },
            estimate: {
              bsonType: 'string'
            },
            currency: {
              bsonType: 'string'
            },
            metadata: {
              bsonType: 'object',
              title: 'metadata',
              required: ['lock_version', 'created_at', 'updated_at'],
              properties: {
                lock_version: {
                  bsonType: 'int'
                },
                created_at: {
                  bsonType: 'date'
                },
                updated_at: {
                  bsonType: 'date'
                }
              }
            }
          }
        }
      }
    });
    db.earnings.createIndex({
      "ticker": 1
    }, {
      name: "earnings_ix_ticker",
      unique: true
    });
}

function create_tracking(db) {
    db.createCollection('task_tracking', {
      validator: {
        $jsonSchema: {
          bsonType: 'object',
          title: 'task_tracking',
          required: ['master_loaded', 'cik_loaded', 'figi_loaded', 'earnings_file_loaded', 'metadata'],
          properties: {
            master_loaded: {
              bsonType: 'bool'
            },
            cik_loaded: {
              bsonType: 'bool'
            },
            figi_loaded: {
              bsonType: 'bool'
            },
            earnings_file_loaded: {
              bsonType: 'bool'
            },
            metadata: {
              bsonType: 'object',
              title: 'metadata',
              required: ['lock_version', 'created_at', 'updated_at'],
              properties: {
                lock_version: {
                  bsonType: 'int'
                },
                created_at: {
                  bsonType: 'date'
                },
                updated_at: {
                  bsonType: 'date'
                }
              }
            }
          }
        }
      }
    });
}

function create_database(database_name) {
    db = db.getSiblingDB(database_name);
    db.dropDatabase();

    db = db.getSiblingDB(database_name);

    create_master(db);
    create_gics_sector(db);
    create_earnings_file(db);

    create_company(db);
    create_income_statement(db);
    create_cash_flow_statement(db);
    create_balance_sheet_statement(db);
    create_earnings_statement(db);
    create_tracking(db);
}
