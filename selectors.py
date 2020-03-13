def init_selectors():
    """
    This method in new file is needed to organise other files better
    custom selectors makes it easier to read
    :return: dict of dicts with selectors
    """
    ids = {'login_button': 'login-btn',
           'login_submit': 'loginSubmit',
           'close_diamond_popup': 'closeButPopup',
           'photoSessionIndicator': 'activity-indicator-photosession',
           'ladyEnergy': 'ladyEnergy',
           'photoSessionTimer': 'activity-timer',
           'maxlevel': 'max-handle-level',
           'minlevel': 'min-handle-level',
           'searchOpponent': 'searchForOponent',
           'searchOpponentAgain': 'searchAgainButton',
           'challenge': 'challengeLady',
           'dollars': 'ladyDollars',
           'currentLevel': 'currentLevel',
           'myStyle': 'stat_style_all',
           'myCreativity': 'stat_creativity_all',
           'myDevotion': 'stat_devotion_all',
           'myBeauty': 'stat_beauty_all',
           'myGenerosity': 'stat_generosity_all',
           'myLoyalty': 'stat_loyalty_all'}

    names = {'username': 'login_user',
             'password': 'login_pass'}

    selectors = {'mobilePopUp': 'div>div+a.pop-up-close',
                 'startEmerald': '#startWorkingFtvButton-1 > a',
                 'tryEmerald': '#ftvChanceBox-1 > a',
                 'popUpEmerald': '#popupMessage + div > a',
                 'stopEmerald': '#workingBoxFtv-1 > div.jobProgress + a',
                 'amOfEmeralds': '#popupMessage > span',
                 'enemyLevelInfo': 'div.right>span.small',
                 'myLevelInfo': 'div.left>span.small',
                 'rewardMoney': '#rewardItems span.award-money',
                 'rewardText': '#rewardItems span.title',
                 'challengedLadyID': 'div.right>span.big>a',
                 'enemyStyle': 'div.style>div.value',
                 'enemyCreativity': 'div.creativity>div.value',
                 'enemyBeauty': 'div.beauty>div.value',
                 'enemyGenerosity': 'div.generosity>div.value',
                 'enemyDevotion': 'div.devotion>div.value',
                 'enemyLoyalty': 'div.loyalty>div.value',
                 'challengeFromProfile': 'div>a.buyOutfit.chalange',
                 'cookiesbutton': 'div>a.cc_btn.cc_btn_accept_all'}
    classes = {
        'enemyLevel': 'level',
        'popularityButton': 'fp-button'

    }
    _selectors = {'selectors': selectors,
                  'ids': ids,
                  'names': names,
                  'classes': classes}
    return _selectors
