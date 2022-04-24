<template>
    <div style="border: 1px solid #ccc;">
        <!-- 工具栏 -->
        <Toolbar
            style="border-bottom: 1px solid #ccc"
            :editorId="editorId"
            :defaultConfig="toolbarConfig"
            :mode="mode"
        />
        <!-- 编辑器 -->
        <Editor
            style="height: 300px; overflow-y: hidden;"
            :editorId="editorId"
            :defaultConfig="editorConfig"
            :mode="mode"
            @onChange="onChange"
            @onMaxLength="onMaxLength"
            @onCreated="onCreate"
        />
    </div>
</template>

<script>
import { Editor, Toolbar, getEditor, removeEditor} from '@wangeditor/editor-for-vue'
import { DomEditor } from '@wangeditor/editor'

export default {
    name: 'MyEditor', 
    components: { Editor, Toolbar },
    data() {
        return {
            editorId: 'wangEditor-1', // 定义一个编辑器 id ，要求：全局唯一且不变。重要！！！
            latestContent: [], // 用于存储编辑器最新的内容，onChange 时修改
            toolbarConfig: {
                excludeKeys:[
                    "headerSelect",
                    "insertImage",
                    "insertTable",
                    "group-video",
                    "group-indent",
                    "fullScreen",
                    "group-more-style",
                    "todo",
                    "justifyRight",
                    "fontFamily",
                    "bulletedList",
                    "blockquote",
                    "|",
                    "fontSize",
                    "lineHeight",
                    "emotion",
                ],
                insertKeys:{
                    index:1,
                    keys:['header3']
                }
                
            },  
            editorConfig: {
                placeholder: '请输入内容...',
                MENU_CONF:{
                    uploadImage:{
                        server: this.$API.API_UPLOAD_IMG,
                        fieldName: 'Image',
                        maxFileSize: 20 * 1024 * 1024,
                        maxNumberOfFiles: 10,
                        // customInsert(res,insertFn){
                        //     insertFn(res.data.url)
                        // },
                        onFailed(file,res) {
                            console.log(`${file.name} 上传失败`, res)
                        },
                        // 上传错误，或者触发 timeout 超时
                        onError(file, err, res) {
                            console.log(`${file.name} 上传出错`, err, res)
                        },
                    },
                    insertImage:{
                        onInsertedImage(imageNode) {
                            if (imageNode == null) return

                            // const { src } = imageNode
                            // console.log('inserted image', src)
                        },
                    }
                },
                maxLength:15000,
            },
            mode:"default",
        }
    },
    methods: {
        onChange(editor) {
            // onChange 时获取编辑器最新内容
            this.latestContent = editor.getHtml()
        },
        onCreate(editor){
            const toolbar = DomEditor.getToolbar(editor)
            console.log(toolbar.getConfig().toolbarKeys)
        },
        onMaxLength(){
            this.$message({
                message:'超出文本最大长度',
                type:'warning'
            })
            
        },
        getImgList(){
            const editor = getEditor(this.editorId)
            return editor.getElemsByType('image')
        },
        clear(){
            const editor = getEditor(this.editorId)
            editor.clear()
        }
    },

    mounted(){
    },

    beforeDestroy() {
        const editor = getEditor(this.editorId)
        if (editor == null) return
        editor.destroy() // 组件销毁时，及时销毁编辑器 ，重要！！！
        removeEditor(this.editorId)
    },
}
</script>

<!-- 记得引入 wangEditor css 文件，重要 ！！！ -->
<style src="@wangeditor/editor/dist/css/style.css"></style>
