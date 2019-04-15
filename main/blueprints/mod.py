#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/4/15 0015 17:15
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import Blueprint, flash, redirect, request, abort
from flask_login import login_required

from main.models.photo import Advice
from main.plugins.decorators import permission_required
from main.plugins.extensions import db

mod_bp = Blueprint('mod', __name__)


@mod_bp.route('/set-advice/<int:advice_id>', methods=['POST'])
@login_required
@permission_required('ADVICE')
def set_advice(advice_id):
    advice = Advice.query.get_or_404(advice_id)
    status = request.form.get('status')
    if not status:
        return abort(400)
    advice.status = status
    flash(f'状态码已设置为：{status}', 'info')
    db.session.commit()
    return redirect(request.referrer)
