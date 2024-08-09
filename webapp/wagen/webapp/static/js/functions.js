function checkSize() {
  var small = map.getSize()[0] < 600;
  attribution.setCollapsible(small);
  attribution.setCollapsed(small);
}