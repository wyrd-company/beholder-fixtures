"use strict";

function BaseReader() {
  this.baseLabel = "base";
}

BaseReader.prototype.describe = function describe() {
  return this.baseLabel;
};

function DerivedReader() {
  BaseReader.call(this);
  this.ownLabel = "derived";
}

DerivedReader.prototype = Object.create(BaseReader.prototype);
DerivedReader.prototype.constructor = DerivedReader;

DerivedReader.prototype.describeOwn = function describeOwn() {
  return this.ownLabel;
};

module.exports = DerivedReader;
