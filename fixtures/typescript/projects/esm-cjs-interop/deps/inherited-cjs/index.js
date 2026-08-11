"use strict";

const inheritedMarker = "inherited-enumerable";

const exportBag = Object.create({ inheritedMarker });

exportBag.ownMarker = "own-enumerable";

exportBag.readOwn = function readOwn() {
  return exportBag.ownMarker;
};

module.exports = exportBag;
