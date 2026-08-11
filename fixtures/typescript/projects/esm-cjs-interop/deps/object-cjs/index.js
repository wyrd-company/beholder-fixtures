"use strict";

const ownField = "owned";

const record = {
  ownField,
  readOwn() {
    return ownField;
  },
};

module.exports = record;
