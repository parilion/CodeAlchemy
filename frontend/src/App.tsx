import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { Layout, Menu } from 'antd'
import { HomeOutlined, UploadOutlined, RocketOutlined } from '@ant-design/icons'
import Dashboard from './pages/Dashboard'
import UploadProject from './pages/UploadProject'
import ConfigureAI from './pages/ConfigureAI'
import TemplateGen from './pages/TemplateGen'

const { Header, Content } = Layout

export default function App() {
  return (
    <BrowserRouter>
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{ display: 'flex', alignItems: 'center', padding: '0 24px' }}>
          <div style={{ color: 'white', fontWeight: 'bold', fontSize: 16, marginRight: 32 }}>
            AI赋能平台
          </div>
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['home']}
            style={{ flex: 1, border: 'none' }}
            items={[
              { key: 'home', icon: <HomeOutlined />, label: <Link to="/">首页</Link> },
              { key: 'upload', icon: <UploadOutlined />, label: <Link to="/upload">代码增强</Link> },
              { key: 'template', icon: <RocketOutlined />, label: <Link to="/template">模板生成</Link> },
            ]}
          />
        </Header>
        <Content style={{ background: '#f5f5f5' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<UploadProject />} />
            <Route path="/configure" element={<ConfigureAI />} />
            <Route path="/template" element={<TemplateGen />} />
          </Routes>
        </Content>
      </Layout>
    </BrowserRouter>
  )
}
