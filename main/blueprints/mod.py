#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/4/15 0015 17:15
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import Blueprint, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user

from main.models.photo import Comment, Advice
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


@mod_bp.route('/advice', methods=['POST'])
@login_required
@permission_required('ADVICE')
def advice():
    body = request.form.get('body')
    depart_id = request.form.get('depart_id')
    passed_count = request.form.get('passed_count')
    url = request.form.get('url')
    filter = request.form.get('filter')
    advice = Advice(depart_id=depart_id,
                    passed_count=passed_count,
                    url=url,
                    filter=filter,
                    author=current_user._get_current_object())
    comment = Comment(body=body,
                      advice=advice,
                      author=current_user._get_current_object())
    db.session.add(advice, comment)
    db.session.commit()
    flash('评论成功！', 'success')
    return redirect(url_for('ins.photos_list_advice'))
