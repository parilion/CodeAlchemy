import { Upload, Steps, message, Typography } from 'antd'
import { InboxOutlined } from '@ant-design/icons'
import { useState } from 'react'
import { uploadProject } from '../api/client'
import { useProjectStore } from '../store/useProjectStore'
import { useNavigate } from 'react-router-dom'

export default function UploadProject() {
  const [loading, setLoading] = useState(false)
  const { setProjectId } = useProjectStore()
  const nav = useNavigate()

  const handleUpload = async (file: File) => {
    setLoading(true)
    try {
      const res = await uploadProject(file)
      setProjectId(res.data.project_id)
      message.success('项目上传成功，请选择AI功能模块')
      nav('/configure')
    } catch {
      message.error('上传失败，请重试')
    } finally {
      setLoading(false)
    }
    return false
  }

  return (
    <div style={{ padding: 32, maxWidth: 800, margin: '0 auto' }}>
      <Steps
        current={0}
        style={{ marginBottom: 32 }}
        items={[
          { title: '上传项目' },
          { title: '选择AI模块' },
          { title: '下载结果' },
        ]}
      />
      <Typography.Title level={4}>上传 Spring Boot 项目</Typography.Title>
      <Upload.Dragger
        beforeUpload={handleUpload}
        accept=".zip"
        disabled={loading}
        showUploadList={false}
      >
        <p><InboxOutlined style={{ fontSize: 48, color: '#1677ff' }} /></p>
        <p style={{ fontSize: 16 }}>点击或拖拽上传项目 ZIP 包</p>
        <p style={{ color: '#999' }}>支持 Spring Boot 2.x / 3.x 项目</p>
      </Upload.Dragger>
      {loading && <p style={{ textAlign: 'center', marginTop: 16 }}>正在上传...</p>}
    </div>
  )
}
