/* 源文件：https://www.biliplus.com/js/bottomscript.js
   页面通用 js
*/

'use strict';
(function () {
	var slice = [].slice;
	Array.from = function (a) { return slice.call(a); };
	!window.requestAnimationFrame && (window.requestAnimationFrame = webkitRequestAnimationFrame || mozRequestAnimation || function (a) { return setTimeout(a, 1e3 / 60); });
	window.gEle = function (e) { return document.getElementById(e); };
	window.blankImg = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==';
	var noticeArr = [],
		slideoutNotice = function (notice) {
			if (notice.parentNode) {
				notice.style.transition = 'top .5s';
				notice.style.top = '-100px';
				setTimeout(function () { removeNotice(notice); }, 510);
			}
		},
		removeNotice = function (notice) {
			var index = noticeArr.indexOf(notice);
			if (index === -1) return false;
			noticeArr.splice(index, 1);
			notice.remove();
		};
	window.createUpdateNotice = function (notice, color, stayOnScreen, dismissCallback) {
		color = '#' + color;
		var noticeDiv = _('div', {
			class: "Biliplus-Notice",
			style: { background: color },
			event: {
				click: function () {
					removeNotice(this);
				}
			}
		});
		if (typeof (notice) == 'string') {
			noticeDiv.innerHTML = notice;
		}
		document.body.appendChild(noticeDiv);
		var top = noticeArr.length ? noticeArr[noticeArr.length - 1].nextTop : 50,
			height = noticeDiv.offsetHeight;
		noticeDiv.style.top = top + 'px';
		noticeDiv.nextTop = top + height + 20;
		noticeDiv.appendChild(_('div', {
			className: 'after', style: {
				borderWidth: 'calc(' + height + 'px / 2) 5px',
				borderRightColor: color,
				borderBottomColor: color
			}
		}));
		noticeArr.push(noticeDiv);
		stayOnScreen !== true ? setTimeout(function () {
			slideoutNotice(noticeDiv);
		}, 5e3) :
			typeof dismissCallback == 'function' && (noticeDiv.addEventListener('click', dismissCallback), noticeDiv.style.cursor = 'pointer');
		/*if(gEle("updateNotice")!=null){
			document.body.removeChild(gEle("updateNotice"));
			clearTimeout(removeTimeout);
		}
		var updateNoticeDiv=document.createElement("div");
		document.body.appendChild(updateNoticeDiv);
		updateNoticeDiv.outerHTML='<div id="updateNotice" style="position:fixed;left:0;right:0;top:0;height:0;z-index:105;transition:.5s"><div style="opacity:.8;position:absolute;bottom:0;left:0;right:0;padding:10px;background-color:#'+color+';color:#fff;text-align:center;font-size:15px"><p style="margin:0;padding:0;">'+noticeText+'</p><a style="position:absolute;right:12px;top:50%;font-size:20px;color:#fff;margin:0;padding:0;;margin-top:-10px;line-height:20px;cursor:pointer;" onclick="removeUpdateNotice();">×</a></div></div>';
		setTimeout(function(){
			gEle('updateNotice').style.height=(gEle('updateNotice').childNodes[0].offsetHeight-1)+'px';
		},10);
		removeTimeout=setTimeout(removeUpdateNotice,5000);*/
	};
	window.removeUpdateNotice = function () {
		noticeArr.forEach(function (i) {
			slideoutNotice(i);
		});
	};
	/*
	var titleOffset=0;
	var titleDisabled=(canls && localStorage.noTitleScroll=='on');
	window.disableTitle = function(s){
		title(0);
		document.title=titletext;
		titleDisabled=s;
	}
	window.title=function(reset){
		if(reset==0){
			titleOffset=0;
			document.title=titletext
			return;
		}
		if(titleDisabled){
			return;
		}
		var offset=titleOffset+=250,charOff=Math.round(offset/250),len=titletext.length;
		charOff-=20;
		if(charOff<=0)charOff=0;
		while(titletext.substr(charOff,1).trim()==''){
			charOff++;
			titleOffset+=250;
		}
		if(charOff>=len-12){
			charOff=0;
			titleOffset=0;
		}
		document.title=titletext.substr(charOff);
	};
	window.addEventListener('DOMContentLoaded',function(){titletext=document.title;title(0);setInterval(title,250)});
	window.addEventListener('beforeunload',function(){titleOffset=0;document.title=titletext});
	var timerChk=function(){
		var now=Date.now(),nowFront=( (now-timerChk.prev) < 500 );
		if(!nowFront)
			titleOffset=0;
		timerChk.prev=now;
	}
	timerChk.prev=Date.now();
	window.titleTimer=null;
	setInterval(timerChk,250);*/
	window.disableTitle = window.title = function () { document.title = titletext; };
	window.loadScript = function (param, id) {
		if (param == undefined) return false;
		var script = document.createElement('script');
		if (typeof (param) == 'string')
			script.src = param;
		else if (typeof (param) == 'object') {
			if (param.src == undefined) return false;
			script.src = param.src;
			if (param.id != undefined)
				script.id = param.id;
			if (param.error != undefined)
				script.setAttribute('onerror', param.error);
		}
		if (id != undefined) script.id = id;
		document.body.appendChild(script);
	};
	/* 2019-1-16 11:47:23
	window.imgClick = function () {
		var imgs = gEle('content').getElementsByTagName('img'), i = 0, img;
		for (; i < imgs.length; i++) {
			img = imgs[i];
			if (!img.hasAttribute('nolink') && !img.BP_viewimgAdded)
				img.addEventListener("click", viewimg), img.BP_viewimgAdded = true;
		}
	};
	*/
	var fixImg = function () {
		if (/(hdslb\.com|img\.biliplus\.com)/.test(this.src)) {
			if (/@.*?jpg$/.test(this.src)) {
				return this.src = this.src.replace(/@.*?jpg$/, '');
			}
			this.src += '@jpg';
			this.removeEventListener('error', fixImg);
		}
	}
	var fixImgObserver = new MutationObserver(function () {
		var imgs = document.getElementsByTagName('img');
		for (var i = 0; i < imgs.length; i++) {
			if (!imgs[i].setFixer) {
				imgs[i].setFixer = true;
				imgs[i].addEventListener('error', fixImg);
			}
		}
	});
	fixImgObserver.observe(document, { childList:true, subtree: true });
	function viewimg_touchmove(e) {
		e.preventDefault();
		e.stopPropagation();
		return false;
	}
	function viewimg(e) {
		var ele = this;
		var origLoader = null;
		var close = function (e) {
			if (this.nodeName.toLowerCase() == 'td') {
				if (e.target != this) return;
			}
			if (origLoader != null) {
				origLoader.abort();
			}
			img.zoomObj.destroy();
			viewImgContainer.remove();
			document.body.style.overflow = '';
		};
		var viewImgContainer = document.body.appendChild(_('div', { className: 'container', style: { opacity: 1, overflowX: 'hidden', overflowY: 'auto', left: 0, top: 0 } }, [
			_('table', { className: 'white_container', style: { display: 'table', textAlign: 'center', position: 'initial', background: 'rgba(0,0,0,.7)' }, event: { touchmove: viewimg_touchmove } }, [_('tbody', {}, [_('tr', {}, [_('td', { event: { click: close } }, [_('span', {}, [_('img', { src: this.src, style: { maxWidth: '100%', verticalAlign: 'bottom' }, event: { click: function () { window.open(this.hasAttribute('original-src') ? this.getAttribute('original-src') : this.src) } } })])])])])]),
			_('div', {
				style: {
					position: 'fixed',
					top: '25px',
					right: '25px',
					zIndex: 1,
					background: 'rgba(255,255,255,.3)',
					borderRadius: '10px'
				},
				event: { click: close }
			})
		]));
		viewImgContainer.children[1].innerHTML = '<svg width="30" height="30" style="display:block;fill:#000;stroke:#000"><path d="M8,6L24,22L22,24L6,8" /><path d="M22,6L6,22L8,24L24,8" /></svg>';
		var img = viewImgContainer.querySelector('img');
		img.zoomObj = new Zoom(img);
		if (ele.hasAttribute('original-src')) {
			var progressBar = viewImgContainer.appendChild(_('div', { className: 'img-progress', style: { width: '5px' } })), url = ele.getAttribute('original-src');
			setTimeout(function () {
				//img.src = ele.getAttribute('original-src');
				if (/https:\/\/(i\d\.hdslb\.com|[\w\.]+\.biliplus\.com)\//.test(url)) {
					var xhr = new XMLHttpRequest();
					origLoader = xhr;
					xhr.open('GET', url, true);
					xhr.onprogress = function (e) { progressBar.style.width = (e.loaded / e.total) * 100 + '%'; };
					xhr.onload = function () {
						origLoader = null;
						url = URL.createObjectURL(xhr.response)
						img.src = url;
						img.setAttribute('original-src', ele.getAttribute('original-src'));
						progressBar.style.width = '100%';
						progressBar.style.opacity = 0;
					};
					xhr.responseType = 'blob';
					xhr.send();
				} else {
					img.src = ele.getAttribute('original-src');
				}
			}, 100);
			img.addEventListener('load', function () {
				if (this.currentSrc != url) return;
				progressBar.style.width = '100%';
				progressBar.style.opacity = 0;
				this.sizeChanged = true;
				this.zoomObj.reset();
				url.substr(0, 5) == 'blob:' && URL.revokeObjectURL(url);
			});
		}
		document.body.style.overflow = 'hidden';
		e.stopPropagation();
	}
	window.viewimg = viewimg;
	// imgClick();

	String.prototype.recursiveReplace = function (replace) {
		var replacements = [], str = this;
		replace.forEach(function (i) {
			str = str.replace(i[0], function () {
				return '$replacement' + (replacements.push( i[1].apply(str, arguments) ) - 1) + '$';
			});
		});
		return str.replace(/\$replacement(\d+)\$/g, function (s, id) {
			return replacements[id];
		});
	}
	/**
	 * zoom.js
	 * https://github.com/anitasv/zoom
	 */

	// Type Vector is [ x, y ]
	// Type Matrix is [ Vector, Vector ]
	// Type Transform is [ Matrix, Vector ]

	/**
	 * Multiply Scalar with Vector returns a Vector.
	 * 
	 * @param {number} l scalar to multiply with
	 * @param {Array<number>} x 2D vector.
	 * @return {Array<number>}
	 */
	var scmult = function (l, x) {
		return [l * x[0], l * x[1]];
	};

	/**
	* Adding two vectors is another vector.
	* 
	* @param {Array<number>} a 2D vector.
	* @param {Array<number>} b 2D vector.
	* @return {Array<number>} Sum vector.
	*/
	var vcadd = function (a, b) {
		return [a[0] + b[0], a[1] + b[1]];
	};

	/**
	* Get the length of vector.
	* 
	* @param {Array<number>} x 2D vector.
	* @return {number} vector length.
	*/
	var vcLength = function (x) {
		return Math.sqrt(x[0] * x[0] + x[1] * x[1]);
	};

	/**
	* Get the angle of vector.
	* 
	* @param {Array<number>} x 2D vector.
	* @return {number} vector length.
	*/
	var vcAngle = function (x) {
		var length = vcLength(x), angle = Math.acos(x[0] / length);
		if (x[1] < 0)
			angle = Math.PI * 2 - angle;
		return angle;
	};

	/**
	* Subtracting two vectors is another vector.
	* 
	* @param {Array<number>} a 2D vector.
	* @param {Array<number>} b 2D vector.
	* @return {Array<number>} Difference vector.
	*/
	var minus = function (a, b) {
		return [a[0] - b[0], a[1] - b[1]];
	};

	/**
	* Dot product of two vectors is scalar.
	* 
	* @param {Array<number>} a 2D vector.
	* @param {Array<number>} b 2D vector.
	* @return {number} scalar inner product.
	*/
	var dot = function (a, b) {
		return a[0] * b[0] + a[1] * b[1];
	};

	/**
	* Exterior Product of two vectors is a pseudoscalar.
	* 
	* @param {Array<number>} a 2D vector.
	* @param {Array<number>} b 2D vector.
	* @return {number} psuedo-scalar exterior product.
	*/
	var wedge = function (a, b) {
		return a[0] * b[1] - a[1] * b[0];
	};

	/**
	* Apply Matrix on Vector returns a Vector.
	* 
	* @param {Array<Array<number>>} A 2x2 Matrix
	* @param {Array<number>} x 2D vector.
	* @return {Array<number>} 2D vector linear product.
	*/
	var apply = function (A, x) {
		return vcadd(scmult(x[0], A[0]), scmult(x[1], A[1]));
	};

	/**
	* Multiply two matrices.
	* 
	* @param {Array<Array<number>>} A 2x2 Matrix
	* @param {Array<Array<number>>} B 2x2 Matrix
	* @return {Array<Array<number>>} A 2x2 Matrix
	*/
	var mult = function (A, B) {
		return [apply(A, B[0]), apply(A, B[1])];
	};

	/**
	* Represents a transform operation, Ax + b
	* 
	* @constructor
	* 
	* @param {Array<Array<number>>} A 2x2 Matrix.
	* @param {Array<number>} b 2D scalar.
	*/
	function Transform(A, b) {
		this.A = A;
		this.b = b;
	}

	/**
	* Given CSS Transform representation of the class.
	* @return {string} CSS 2D Transform. 
	*/
	Transform.prototype.css = function () {
		var A = this.A;
		var b = this.b;
		return 'matrix(' + A[0][0] + ',' + A[0][1] + ',' + A[1][0] + ',' + A[1][1] +
			',' + b[0] + ',' + b[1] + ')';
	};

	/**
	* Multiply two transforms. 
	* Defined as 
	*  (T o U) (x) = T(U(x))
	* 
	* Derivation:
	*  T(U(x)) 
	*   = T(U.A(x) + U.b) 
	*   = T.A(U.A(x) + U.b)) + T.b
	*   = T.A(U.A(x)) + T.A(U.b) + T.b 
	* 
	* @param {Transform} T 
	* @param {Transform} U 
	* @return {Transform} T o U
	*/
	var cascade = function (T, U) {
		return new Transform(mult(T.A, U.A), vcadd(apply(T.A, U.b), T.b));
	};

	/**
	* Creates the default rotation matrix
	* 
	* @param {number} c x-projection (r cos(theta))
	* @param {number} s y-projection (r sin(theta))
	* @return {Array<Array<number>>} Rotation matrix.
	*/
	var rotate = function (c, s) {
		return [[c, s], [-s, c]];
	};

	/**
	* Returns matrix that transforms vector a to vector b.
	* 
	* @param {Array<number>} a 2D vector.
	* @param {Array<number>} b 2D vector.
	* @return {Array<Array<number>>} Rotation + Scale matrix
	*/
	var rotscale = function (a, b) {
		var alen = dot(a, a);
		var sig = dot(a, b);
		var del = wedge(a, b);
		return rotate(sig / alen, del / alen);
	};

	var justscale = function (a, b) {
		var alen = Math.sqrt(dot(a, a));
		var blen = Math.sqrt(dot(b, b));
		var scale = blen / alen;
		return rotate(scale, 0)
	};

	/**
	* Zoom is a similarity preserving transform from a pair of source
	* points to a new pair of destination points. If rotate it is false
	* then it won't be maintaining the transfer precisely, but will only
	* do scaling part of it.
	* 
	* @param {Array<Array<number>>} s two source points.
	* @param {Array<Array<number>>} d two destination points.
	* @param {Boolean} rotate true - rotate; else scale.
	* 
	* @return {Transform} that moves point 's' to point 'd' 
	*/
	var zoom = function (s, d, rotate) {
		// Source vector.
		var a = minus(s[1], s[0]);
		// Destination vector.
		var b = minus(d[1], d[0]);
		// Rotation needed for source to dest vector.
		var rs = rotate ? rotscale(a, b) : justscale(a, b);

		// Position of s[0] if rotation is applied.
		var rs0 = apply(rs, s[0]);
		// Since d[0] = rs0 + t
		var t = minus(d[0], rs0);

		return new Transform(rs, t);
	};

	/**
	* Weighted average of two vectors.
	* 
	* @param {Array<number>} u 2D vector.
	* @param {Array<number>} v 2D vector.
	* @param {number} progress (from 0 to 1)
	* @return {Array<number>} (1-p) u + (p) v 
	*/
	var avgVector = function (u, v, progress) {
		var u1 = scmult(1 - progress, u);
		var v1 = scmult(progress, v);
		return vcadd(u1, v1);
	};

	/**
	* Weighted average of two vectors.
	* 
	* @return {Array<Array<number>>} A 2D matrix.
	* @return {Array<Array<number>>} B 2D matrix.
	* @param {number} progress (from 0 to 1)
	* @return {Array<Array<number>>} (1-p) A + (p) B 
	*/
	var avgMatrix = function (A, B, progress) {
		return [avgVector(A[0], B[0], progress), avgVector(A[1], B[1], progress)];
	};


	/**
	* Weighted average of two transforms.
	* @param {Transform} Z Source Transform
	* @param {Transform} I Destination Transform
	* @param {number} progress (from 0 to 1)
	* @return {Transform} (1-p) Z + (p) I 
	*/
	Transform.avg = function (Z, I, progress) {
		return new Transform(avgMatrix(Z.A, I.A, progress), avgVector(Z.b, I.b, progress));
	};

	var identity = new Transform([[1, 0], [0, 1]], [0, 0]);

	/**
	* Gives a default value for an input object.
	* 
	* @param {Object} param input parameter, may be undefined
	* @param {Object} val returned if param is undefined.
	* @return {Object}
	*/
	var defaults = function (param, val) {
		return (param == undefined) ? val : param;
	};

	/**
	* Method to override json config objects with default
	* values. If undefined in cfg corresponding value from
	* cfg_def will be picked.
	* 
	* @param {Object} cfg input parameter config.
	* @param {Object} cfg_def default fallbacks.
	* @return {Object} new config
	*/
	var default_config = function (cfg, cfg_def) {
		var new_cfg = defaults(cfg, {})
		for (var k in cfg_def) {
			new_cfg[k] = defaults(new_cfg[k], cfg_def[k])
		}
		return new_cfg;
	};

	/**
	* @constructor
	* @export
	* @param {Element} elem to attach zoom handler.
	* @param {Object} config to specify additiona features.
	*/
	function Zoom(elem, config, wnd) {
		this.mayBeDoubleTap = null;
		this.isAnimationRunning = false;
		this.runningRequest = null;
		// SingleFinger = 1, DoubleFinger = 2, NoTouch = 0
		this.curTouch = 0;
		this.elem = elem;
		this.activeZoom = identity;
		this.resultantZoom = identity;

		this.srcCoords = [0, 0];
		this.destCoords = [0, 0];
		var me = this;

		this.config = default_config(config, {
			"pan": false,
			"rotate": true
		});

		this.wnd = wnd || window;

		elem.style['transform-origin'] = 'center';

		var getCoordsDouble = function (t) {
			var oX = elem.offsetLeft + initialSize[0] / 2;
			var oY = elem.offsetTop + initialSize[1] / 2;
			return [
				[t[0].clientX - oX, t[0].clientY - oY],
				[t[1].clientX - oX, t[1].clientY - oY]
			];
		};

		var getCoordsSingle = function (t) {
			var oX = elem.offsetLeft;
			var oY = elem.offsetTop;
			var x = t[0].clientX - oX;
			var y = t[0].clientY - oY;
			return [
				[x, y],
				[x + 1, y + 1]
			];
		};

		var getCoords = function (t) {
			return t.length > 1 ? getCoordsDouble(t) : getCoordsSingle(t);
		};

		var setSrcAndDest = function (touches) {
			me.srcCoords = getCoords(touches);
			me.destCoords = me.srcCoords;
		};

		var setDest = function (touches) {
			me.destCoords = getCoords(touches);
		};

		var handleTouchEvent = function (cb) {
			return function (evt) {
				evt.preventDefault();
				if (me.isAnimationRunning) {
					me.runningRequest && cancelAnimationFrame(me.runningRequest);
					me.runningRequest = null;
					me.isAnimationRunning = false;
				}
				var touches = evt.touches;
				if (!touches) {
					return false;
				}
				cb(touches);
			};
		};

		var translating = false, verSmaller = true, hozSmaller = true, resetAfterEnd = false;

		var handleZoom = handleTouchEvent(function (touches) {
			var numOfFingers = touches.length;
			if (numOfFingers != me.curTouch) {
				me.curTouch = numOfFingers;
				me.finalize();
				if (numOfFingers != 0) {
					setSrcAndDest(touches);
				}
			} else if (touches.length) {
				setDest(touches);
				if (translating) {
					if (hozSmaller) {
						me.destCoords[0][0] = me.srcCoords[0][0];
						me.destCoords[1][0] = me.srcCoords[1][0];
					}
					if (verSmaller) {
						me.destCoords[0][1] = me.srcCoords[0][1];
						me.destCoords[1][1] = me.srcCoords[1][1];
					}
				}
				if (preventRotate) {
					var angle = vcAngle(zoom(me.srcCoords, me.destCoords, true).A[0]);
					if (angle < Math.PI / 12 || angle > Math.PI * 23 / 12) {
						//旋转小于30度时取消旋转
						me.config.rotate = false;
					} else {
						preventRotate = false;
						me.config.rotate = true;
					}
				}
				me.previewZoom();
			}
			if (touches.length == 1) {
				oldTouch = [touches[0].clientX, touches[0].clientY];
			}
		});

		var oldTouch, oldTrack, speedTracker;

		var speedTrack = function () {
			var t = Date.now();
			if (t == oldTrack.time) return;
			var delta = minus(oldTouch, oldTrack.vec);
			oldTrack.speed = scmult(200 / (t - oldTrack.time), delta);
			oldTrack.vec = oldTouch;
			oldTrack.time = t;
		};

		var initialSize = null, initialOffset = null, startAngle = null, preventRotate = true;

		var handleTouchStart = handleTouchEvent(function (touches) {
			translating = touches.length == 1;
			if (initialSize == null || elem.sizeChanged) {
				initialSize = [elem.offsetWidth, elem.offsetHeight];
				hozSmaller = initialSize[0] < innerWidth;
				verSmaller = initialSize[1] < innerHeight;
				var box = elem.getBoundingClientRect();
				initialOffset = [box.left, box.top];
				elem.sizeChanged = false;
			}
			if (!speedTracker) {
				speedTracker = setInterval(speedTrack, 50);
				oldTouch = [touches[0].clientX, touches[0].clientY];
				oldTrack = { speed: [0, 0], vec: oldTouch, time: Date.now() };
			}
			if (startAngle == null) {
				var cos = me.resultantZoom.A[0][0], sin = me.resultantZoom.A[0][1];
				startAngle = (cos ? (cos > 0 ? 0 : 2) : (sin > 0 ? 1 : 3)) * Math.PI / 2;
				preventRotate = true;
			}
			if (touches.length === 1) {
				if (me.mayBeDoubleTap != null) {
					resetAfterEnd = true;
				} else {
					me.mayBeDoubleTap = me.wnd.setTimeout(function () {
						me.mayBeDoubleTap = null;
					}, 300);
				}
			}
		});
		var handleTouchEnd = handleTouchEvent(function (touches) {
			translating = false;
			if (touches.length === 1) oldTouch = [touches[0].clientX, touches[0].clientY], oldTrack.vec = oldTouch;
			if (touches.length === 0) {
				clearInterval(speedTracker);
				speedTracker = null;
				startAngle = null;
				/**
				 * reset rotation to n*90deg
				 * move in to the border, if smaller than container, center align
				 */
				var length = vcLength(me.activeZoom.A[0]),
					angle = vcAngle(me.activeZoom.A[0]),
					angleSector = angle / Math.PI * 2,
					originAngle = vcAngle(initialSize),
					centralPoint = [initialOffset[0] + initialSize[0] / 2, initialOffset[1] + initialSize[1] / 2],
					animate = false;
				if ((angleSector % 1) != 0) animate = true;
				angleSector = Math.round(angleSector) % 4;
				var cosFactor = [1, 0, -1, 0], sinFactor = [0, 1, 0, -1];
				var translate = vcadd(me.activeZoom.b, oldTrack.speed);
				//mininal scale is 1x
				if (length < 1) length = 1;
				//position center
				hozSmaller = false;
				verSmaller = false;
				if (angleSector % 2) {
					//rotation 90/270deg
					if (initialSize[1] * length < window.innerWidth) {
						translate[0] = innerWidth / 2 - centralPoint[0];
						hozSmaller = true;
					} else if (Math.abs(translate[0] + innerWidth / 2 - centralPoint[0]) * 2 + innerWidth > initialSize[1] * length) {
						translate[0] = (initialSize[1] * length - innerWidth) / ((translate[0] > 0) ? 2 : -2) + innerWidth / 2 - centralPoint[0];
					}
					if (initialSize[0] * length < window.innerHeight) {
						translate[1] = innerHeight / 2 - centralPoint[1];
						verSmaller = true;
					} else {
						if (translate[1] > (initialSize[0] * length) / 2 - centralPoint[1])
							translate[1] = (initialSize[0] * length) / 2 - centralPoint[1];
						else if (translate[1] < (innerHeight - centralPoint[1]) - (initialSize[0] * length / 2))
							translate[1] = (innerHeight - centralPoint[1]) - (initialSize[0] * length / 2);
					}
				} else {
					//rotation 0/180deg
					if (initialSize[0] * length < window.innerWidth) {
						translate[0] = innerWidth / 2 - centralPoint[0];
						hozSmaller = true;
					} else if (Math.abs(translate[0]) * 2 + innerWidth > initialSize[0] * length) {
						translate[0] = (initialSize[0] * length - innerWidth) / ((translate[0] > 0) ? 2 : -2);
					}
					if (initialSize[1] * length < window.innerHeight) {
						translate[1] = innerHeight / 2 - centralPoint[1];
						verSmaller = true;
					} else {
						if (translate[1] > (initialSize[1] * length) / 2 - centralPoint[1])
							translate[1] = (initialSize[1] * length) / 2 - centralPoint[1];
						else if (translate[1] < (innerHeight - centralPoint[1]) - (initialSize[1] * length / 2))
							translate[1] = (innerHeight - centralPoint[1]) - (initialSize[1] * length / 2);
					}
				}
				if (translate[0] != me.activeZoom.b[0] || translate[1] != me.activeZoom.b[1]) animate = true;

				animate ? me.reset(new Transform(
					[
						[length * cosFactor[angleSector], length * sinFactor[angleSector]],
						[-length * sinFactor[angleSector], length * cosFactor[angleSector]]
					],
					translate
				)) : (resetAfterEnd && (me.reset(), resetAfterEnd = false));
			}
		});

		elem.parentNode.addEventListener('touchstart', handleTouchStart);
		elem.parentNode.addEventListener('touchstart', handleZoom);
		elem.parentNode.addEventListener('touchmove', handleZoom);
		elem.parentNode.addEventListener('touchend', handleZoom);
		elem.parentNode.addEventListener('touchend', handleTouchEnd);

		var moved = false, isSingleFinger = true;
		elem.addEventListener('touchstart', function (e) { if (e.touches.length > 1) return (isSingleFinger = false, void 0); moved = false; });
		elem.addEventListener('touchmove', function (e) { if (e.touches.length > 1) return; moved = true; });
		elem.addEventListener('touchend', function (e) {
			if (e.touches.length > 0) return;
			if (moved) clearTimeout(me.mayBeDoubleTap), me.mayBeDoubleTap = null;
			if (!moved && isSingleFinger && vcLength(me.activeZoom.A[0]) == 1)
				window.open(elem.hasAttribute('original-src') ? elem.getAttribute('original-src') : elem.src);
			isSingleFinger = true;
		});
		var resize = function () {
			elem.sizeChanged = true;
			me.setZoom(identity);
		};
		window.addEventListener('resize', resize);

		this.destroy = function () {
			window.removeEventListener('resize', resize);
		};
	}

	Zoom.prototype.previewZoom = function () {
		var additionalZoom = zoom(this.srcCoords, this.destCoords, this.config.rotate);
		this.resultantZoom = cascade(additionalZoom, this.activeZoom);
		this.repaint();
	};

	Zoom.prototype.setZoom = function (newZoom) {
		this.resultantZoom = newZoom;
		this.repaint();
	};

	Zoom.prototype.finalize = function () {
		this.activeZoom = this.resultantZoom;
	};

	Zoom.prototype.repaint = function () {
		this.elem.style.transform = this.resultantZoom.css();
	};

	Zoom.prototype.reset = function (final) {
		var duration = 300;
		if (final == undefined)
			final = identity, duration = 100;
		if (this.wnd.requestAnimationFrame) {
			this.isAnimationRunning = true;
			var Z = this.activeZoom;
			var startTime = null;

			var me = this;

			var step = function (time) {
				if (!startTime) {
					startTime = time;
				}
				var progress = Math.atan((time - startTime) / duration * 5) / 1.38;
				if (progress >= 1) {
					me.setZoom(final);
					me.isAnimationRunning = false;
					me.runningRequest = null;
				} else {
					me.setZoom(Transform.avg(Z, final, progress));
					me.runningRequest = me.wnd.requestAnimationFrame(step);
				}
			};
			this.runningRequest = this.wnd.requestAnimationFrame(step);
		} else {
			this.setZoom(final);
		}
	};
	Zoom.prototype['reset'] = Zoom.prototype.reset;
	if (typeof exports === "undefined") {
		window['Zoom'] = Zoom;
	} else {
		exports['Zoom'] = Zoom;
	}

	window.getjson = function (url, callback, extraParam) {
		var xmlhttp = new XMLHttpRequest();
		xmlhttp.onreadystatechange = function () {
			if (xmlhttp.readyState == 4) {
				if (xmlhttp.status == 200) {
					if (xmlhttp.response.substr(0, 1) == '{' && xmlhttp.response.substr(-1, 1) == '}')
						callback(JSON.parse(xmlhttp.response), extraParam);
					else
						callback({ "code": -502, "message": "网络错误" }, extraParam);
				} else {
					callback({ "code": -502, "message": "网络错误" }, extraParam);
				}
			}
		};
		xmlhttp.open("GET", url, true);
		xmlhttp.withCredentials = true;
		xmlhttp.send();
		return xmlhttp;
	};
	window.postjson = function (url, callback, body, extraParam, doNotSend) {
		var xhr = new XMLHttpRequest();
		xhr.onreadystatechange = function () {
			if (xhr.readyState == 4) {
				if (xhr.status == 200) {
					if (xhr.response.substr(0, 1) == '{' && xhr.response.substr(-1, 1) == '}')
						callback(JSON.parse(xhr.response), extraParam);
					else
						callback({ "code": -502, "message": "网络错误" }, extraParam);
				} else {
					callback({ "code": -502, "message": "网络错误" }, extraParam);
				}
			}
		};
		xhr.open('POST', url, true);
		xhr.withCredentials = true;
		typeof body == 'string' && xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		!doNotSend && xhr.send(body);
		return xhr;
	};
	/*
	window.img_lazyload = function () {
		if (canls && localStorage.noPic == 'on') return false;
		var imgs = Array.from(document.getElementsByTagName('img'));
		imgs.forEach(function (i) {
			if (!i.hasAttribute('_src')) return;
			var box = i.getBoundingClientRect();
			if (box.bottom < -100 || box.top > (innerHeight + 100) || box.right < -100 || box.left > (innerWidth + 100))
				return;
			i.setAttribute('src', imgSrcProc(i.getAttribute('_src')));
			i.removeAttribute('_src');
		});
	};
	window.addEventListener('scroll', img_lazyload);
	window.addEventListener('resize', img_lazyload);
	img_lazyload();
*/
	var textAutohideClickListener = function () {
		this.className = "pretext";
		this.removeEventListener("click", textAutohideClickListener);
	};
	window.textAutohide = function () {
		var chktextheight = Array.from(document.getElementsByClassName('checktextheight'));
		chktextheight.forEach(function (i) {
			if (i.offsetHeight > 77) {
				i.addEventListener('click', textAutohideClickListener);
				i.className = 'toomuchtext pretext';
			} else {
				i.className = 'pretext';
			}
		});
	};
	window.imgSrcProc = function (s) {
		var ver, supportPolicy = false;
		if ((ver = navigator.userAgent.match(/Firefox\/(\d+)/)) != null && (ver[1] | 0) >= 52) supportPolicy = true;
		if ((ver = navigator.userAgent.match(/Chrome\/(\d+)/)) != null && (ver[1] | 0) >= 61) supportPolicy = true;
		return s.replace(/(https?:)?\/\/i([012])\.hdslb\.com/, function (s, a, b) {
			return supportPolicy ? 'https://i' + b + '.hdslb.com' : 'https://img.biliplus.com';
		});
	};
	window.hasFlash = !1;
	if (navigator.plugins && navigator.plugins['Shockwave Flash'] != undefined) {
		hasFlash = !0;
	}
	window.slide = function (option) {
		var self = this, tracking = null, slideblock, oldTouch, oldTrack, startPos = [], hozMode, ignoreMode,
			start = function (e) {
				slideblock.style.transitionDuration = "";
				if (e.type == 'touchstart') {
					startPos = [e.touches[0].clientX, e.touches[0].clientY];
					oldTouch = startPos[0];
				} else if (e.type == 'mousedown') {
					startPos = [e.clientX, e.clientY];
					oldTouch = startPos[0];
				}
				hozMode = false;
				ignoreMode = false;
				oldTrack = { "X": oldTouch, "time": Date.now(), "speed": 0 };
				slideblock.style.transitionTimingFunction = 'cubic-bezier(.39,.58,.57,1)';
				if (tracking != null)
					clearInterval(tracking);
				tracking = setInterval(speedTrack, 50);
				slideblock.moved = !1;
				if (e.type == 'mousedown') {
					e.preventDefault();
				}
			},
			move = function (e) {
				if (e.touches.length == 1) {
					if (hozMode) {
						e.preventDefault();
					} else if (!ignoreMode) {
						var dx = e.changedTouches[0].clientX - startPos[0], dy = e.changedTouches[0].clientY - startPos[1];
						if (dx < -10 || dx > 10) {
							hozMode = true;
						} else if (dy < -10 || dy > 10) {
							ignoreMode = true;
						}
					}
					var delta = e.changedTouches[0].clientX - oldTouch, rightBorder = -slideblock.scrollWidth + self.width;
					if (rightBorder > 0) rightBorder = 0;
					slideblock.style.transform = 'translateX(' + (self.currentPos + delta) + 'px)';
					self.currentPos = self.currentPos + delta;
					if (self.currentPos > 0) {
						slideblock.style.transform = 'translateX(' + (self.currentPos * .45) + 'px)';
					} else if (self.currentPos < rightBorder) {
						slideblock.style.transform = 'translateX(' + (rightBorder - (rightBorder - self.currentPos) * .45) + 'px)';
					}
					oldTouch = e.changedTouches[0].clientX;
					img_lazyload();
				}
			},
			dragMove = function (e) {
				if (tracking == null)
					return;
				e.preventDefault();
				var delta = e.clientX - oldTouch, rightBorder = -slideblock.scrollWidth + self.width;
				if (rightBorder > 0) rightBorder = 0;
				slideblock.style.transform = 'translateX(' + (self.currentPos + delta) + 'px)';
				self.currentPos = self.currentPos + delta;
				if (self.currentPos > 0) {
					slideblock.style.transform = 'translateX(' + (self.currentPos * .45) + 'px)';
				} else if (self.currentPos < rightBorder) {
					slideblock.style.transform = 'translateX(' + (rightBorder - (rightBorder - self.currentPos) * .45) + 'px)';
				}
				oldTouch = e.clientX;
				slideblock.moved = !0;
				img_lazyload();
			},
			end = function (e) {
				if (tracking == null)
					return;
				var rightBorder = -slideblock.scrollWidth + self.width;
				if (rightBorder > 0) rightBorder = 0;
				if (self.currentPos >= 0) {
					slideblock.style.transitionDuration = '0.5s';
					slideblock.style.transform = 'translate(0px,0px) translateZ(0px)';
					self.currentPos = 0;
				} else if (self.currentPos < rightBorder) {
					slideblock.style.transitionDuration = '0.5s';
					slideblock.style.transform = 'translate(' + rightBorder + 'px,0px) translateZ(0px)';
					self.currentPos = rightBorder;
				} else {
					var finalPos = self.currentPos + (oldTrack.speed * 200);
					if (self.blockWidth > 0)
						finalPos = Math.round((finalPos - (self.width - self.blockWidth) / 2) / self.blockWidth) * self.blockWidth + (self.width - self.blockWidth) / 2;
					if (finalPos > 0) {
						finalPos = 0;
						slideblock.style.transitionTimingFunction = 'cubic-bezier(.18,.89,.32,1.28)';
					}
					if (finalPos < rightBorder) {
						finalPos = rightBorder;
						slideblock.style.transitionTimingFunction = 'cubic-bezier(.18,.89,.32,1.28)';
					}
					slideblock.style.transitionDuration = '0.5s';
					slideblock.style.transform = 'translate(' + finalPos + 'px,0px) translateZ(0px)';
					self.currentPos = finalPos;
					setTimeout(img_lazyload, 4e2);
				}
				clearInterval(tracking);
				tracking = null;
			},
			speedTrack = function () {
				var delta = oldTouch - oldTrack.X;
				oldTrack.speed = delta / (Date.now() - oldTrack.time);
				oldTrack.X = oldTouch;
				oldTrack.time = Date.now();
			};
		if (option.blockWidth == undefined)
			option.blockWidth = 0;
		this.option = option;
		slideblock = option.target;
		this.slideblock = slideblock;
		slideblock.addEventListener('touchstart', start);
		slideblock.addEventListener('touchmove', move);
		slideblock.addEventListener('touchend', end);
		slideblock.addEventListener('mousedown', start);
		window.addEventListener('mousemove', dragMove);
		window.addEventListener('mouseup', end);
		slideblock.style.userSelect = 'none';
		slideblock.style.mozUserSelect = 'none';
		slideblock.style.webkitUserSelect = 'none';
		slideblock.style.msUserSelect = 'none';
		this.currentPos = 0;
		this.width = option.width.target[option.width.prop];
		window.addEventListener('resize', function () { self.width = self.option.width.target[self.option.width.prop]; });
		this.blockWidth = option.blockWidth;
	};

	var timeagoInstance = timeago();
	timeagoInstance.setLocale(({ 'en': 'en', 'zh': 'zh_CN' })[pageConfig.lang]);
	window.timeagoRun = function () {
		var needs = Array.from(document.getElementsByClassName('timeago'));
		needs.forEach(function (i) {
			if (i.hasAttribute('datetime'))
				i.textContent = timeagoInstance.format(i.getAttribute('datetime'));
		});
	};
	setInterval(timeagoRun, 6e4);
	timeagoRun();
})();