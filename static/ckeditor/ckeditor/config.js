/**
 * @license Copyright (c) 2003-2019, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
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
};
