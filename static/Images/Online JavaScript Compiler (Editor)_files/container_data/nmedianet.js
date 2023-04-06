              var _mN = {
    _cid : '8CU63E64Z' || window.medianet_cid || '',
    _crid : '' || window.medianet_crid || '',
    _flping : 'https://lg3.media.net/flping.php?reason=0&action=16&pid=8POX34Y27&gdpr=0'
};
function logFailoverPing() {
    var furl = _mN._flping + '&cid=' + _mN._cid + '&crid=' + _mN._crid;
    (new Image()).src = furl;
}
logFailoverPing();