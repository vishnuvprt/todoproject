/**
<<<<<<< HEAD
 * @license Copyright (c) 2003-2019, CKSource - Frederico Knabben. All rights reserved.
=======
 * @license Copyright (c) 2003-2023, CKSource Holding sp. z o.o. All rights reserved.
>>>>>>> 695c1564f21dc5bb418c10a064dd0137c00b2de9
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
<<<<<<< HEAD
	config.language = 'en';
	// config.uiColor = '#AADC6E';\

	// config.toolbar =
	// 	[
	// 	    [ 'Source', '-', 'Bold', 'Italic' ]
	// 	];

	config.toolbar_Basic =
		[
		   	{ name: 'styles',      items : [ 'Styles','Format','Font','FontSize' ] },
    		{ name: 'colors',      items : [ 'TextColor','BGColor' ] },
    		{ name: 'paragraph',   items : [ 'Source','NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv','-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ] },
    		{ name: 'insert',      items : [ 'Image'] },    		
    		// { name: 'tools',       items : [ 'Maximize', 'ShowBlocks','-','About' ] }
		];
	config.toolbar = 'Basic';
	config.extraPlugins = 'sourcedialog';
=======
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
>>>>>>> 695c1564f21dc5bb418c10a064dd0137c00b2de9
};
