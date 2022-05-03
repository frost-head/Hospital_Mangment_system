
        #     qty += old_qty
        #     insert(mysql, 'update cart set qty = {} where item_id = {} and pid = {}'.format(
        #         qty, item_id, session['user']))
        #     return storeRedirect(item_id, qty)
        # else:
        #     return storeRedirect(item_id, qty)