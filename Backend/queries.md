# GraphQL Queries and Mutations

This document contains all available GraphQL queries and mutations for the VoiceAI backend, along with instructions for connecting to a React frontend.

## GraphQL Endpoint

**URL:** `http://localhost:8000/graphql/` (or your production URL)

**GraphiQL Interface:** Visit `http://localhost:8000/graphql/` in your browser to use the interactive GraphQL explorer.

---

## Available Queries

### 1. Get Projects by Organization

Get all projects for a specific organization.

```graphql
query GetProjectsByOrganization($organizationId: Int!) {
  projectsByOrganization(organizationId: $organizationId) {
    id
    name
    description
    status
    dueDate
    createdAt
    taskCount
    completedTaskCount
    completionRate
    organization {
      id
      name
      slug
      contactEmail
    }
  }
}
```

**Variables:**
```json
{
  "organizationId": 1
}
```

---

### 2. Get Project Statistics

Get comprehensive statistics for all projects in an organization.

```graphql
query GetProjectStatistics($organizationId: Int!) {
  projectStatistics(organizationId: $organizationId) {
    totalProjects
    activeProjects
    completedProjects
    onHoldProjects
    totalTasks
    completedTasks
    inProgressTasks
    todoTasks
    overallCompletionRate
  }
}
```

**Variables:**
```json
{
  "organizationId": 1
}
```

---

### 3. Get Single Project

Get detailed information about a specific project.

```graphql
query GetProject($projectId: Int!) {
  project(projectId: $projectId) {
    id
    name
    description
    status
    dueDate
    createdAt
    taskCount
    completedTaskCount
    completionRate
    organization {
      id
      name
      slug
      contactEmail
    }
  }
}
```

**Variables:**
```json
{
  "projectId": 1
}
```

---

### 4. Get Single Task

Get detailed information about a specific task, including comments.

```graphql
query GetTask($taskId: Int!) {
  task(taskId: $taskId) {
    id
    title
    description
    status
    assigneeEmail
    dueDate
    createdAt
    commentCount
    project {
      id
      name
      status
    }
  }
}
```

**Variables:**
```json
{
  "taskId": 1
}
```

---

## Available Mutations

### 1. Create Project

Create a new project.

```graphql
mutation CreateProject($input: ProjectInput!) {
  createProject(input: $input) {
    success
    errors
    project {
      id
      name
      description
      status
      dueDate
      createdAt
      organization {
        id
        name
      }
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "organizationId": 1,
    "name": "New Project",
    "description": "Project description",
    "status": "active",
    "dueDate": "2024-12-31"
  }
}
```

---

### 2. Update Project

Update an existing project.

```graphql
mutation UpdateProject($projectId: Int!, $input: ProjectUpdateInput!) {
  updateProject(projectId: $projectId, input: $input) {
    success
    errors
    project {
      id
      name
      description
      status
      dueDate
      organization {
        id
        name
      }
    }
  }
}
```

**Variables:**
```json
{
  "projectId": 1,
  "input": {
    "name": "Updated Project Name",
    "status": "completed",
    "description": "Updated description"
  }
}
```

---

### 3. Create Task

Create a new task within a project.

```graphql
mutation CreateTask($input: TaskInput!) {
  createTask(input: $input) {
    success
    errors
    task {
      id
      title
      description
      status
      assigneeEmail
      dueDate
      createdAt
      project {
        id
        name
      }
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "projectId": 1,
    "title": "New Task",
    "description": "Task description",
    "status": "todo",
    "assigneeEmail": "user@example.com",
    "dueDate": "2024-12-31T23:59:59Z"
  }
}
```

---

### 4. Update Task

Update an existing task.

```graphql
mutation UpdateTask($taskId: Int!, $input: TaskUpdateInput!) {
  updateTask(taskId: $taskId, input: $input) {
    success
    errors
    task {
      id
      title
      description
      status
      assigneeEmail
      dueDate
      project {
        id
        name
      }
    }
  }
}
```

**Variables:**
```json
{
  "taskId": 1,
  "input": {
    "title": "Updated Task Title",
    "status": "in_progress",
    "assigneeEmail": "newuser@example.com"
  }
}
```

---

### 5. Add Task Comment

Add a comment to a task.

```graphql
mutation AddTaskComment($input: TaskCommentInput!) {
  addTaskComment(input: $input) {
    success
    errors
    comment {
      id
      content
      authorEmail
      timestamp
      task {
        id
        title
      }
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "taskId": 1,
    "content": "This is a comment on the task",
    "authorEmail": "commenter@example.com"
  }
}
```

---

## Connecting to React Frontend

### Step 1: Install Required Dependencies

```bash
npm install @apollo/client graphql
# or
yarn add @apollo/client graphql
```

### Step 2: Set Up Apollo Client

Create a file `src/apolloClient.js`:

```javascript
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';

const httpLink = createHttpLink({
  uri: 'http://localhost:8000/graphql/', // Change to your backend URL
  credentials: 'same-origin', // Include credentials for CORS
});

const client = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
});

export default client;
```

### Step 3: Wrap Your App with ApolloProvider

In your `src/index.js` or `src/App.js`:

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { ApolloProvider } from '@apollo/client';
import App from './App';
import client from './apolloClient';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ApolloProvider client={client}>
      <App />
    </ApolloProvider>
  </React.StrictMode>
);
```

### Step 4: Use Queries in Components

Example component using the `GetProjectsByOrganization` query:

```javascript
import { useQuery, gql } from '@apollo/client';

const GET_PROJECTS = gql`
  query GetProjectsByOrganization($organizationId: Int!) {
    projectsByOrganization(organizationId: $organizationId) {
      id
      name
      description
      status
      dueDate
      createdAt
      taskCount
      completedTaskCount
      completionRate
    }
  }
`;

function ProjectsList({ organizationId }) {
  const { loading, error, data } = useQuery(GET_PROJECTS, {
    variables: { organizationId },
  });

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <h2>Projects</h2>
      {data.projectsByOrganization.map((project) => (
        <div key={project.id}>
          <h3>{project.name}</h3>
          <p>{project.description}</p>
          <p>Status: {project.status}</p>
          <p>Tasks: {project.taskCount} ({project.completedTaskCount} completed)</p>
          <p>Completion Rate: {project.completionRate}%</p>
        </div>
      ))}
    </div>
  );
}

export default ProjectsList;
```

### Step 5: Use Mutations in Components

Example component using the `CreateProject` mutation:

```javascript
import { useState } from 'react';
import { useMutation, gql } from '@apollo/client';

const CREATE_PROJECT = gql`
  mutation CreateProject($input: ProjectInput!) {
    createProject(input: $input) {
      success
      errors
      project {
        id
        name
        description
        status
        dueDate
      }
    }
  }
`;

function CreateProjectForm({ organizationId, onProjectCreated }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('active');

  const [createProject, { loading, error }] = useMutation(CREATE_PROJECT, {
    onCompleted: (data) => {
      if (data.createProject.success) {
        alert('Project created successfully!');
        onProjectCreated(data.createProject.project);
        // Reset form
        setName('');
        setDescription('');
        setStatus('active');
      } else {
        alert('Error: ' + data.createProject.errors.join(', '));
      }
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    createProject({
      variables: {
        input: {
          organizationId: parseInt(organizationId),
          name,
          description,
          status,
        },
      },
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create New Project</h2>
      <div>
        <label>Name:</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Description:</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>
      <div>
        <label>Status:</label>
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="active">Active</option>
          <option value="completed">Completed</option>
          <option value="on_hold">On Hold</option>
        </select>
      </div>
      <button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Create Project'}
      </button>
      {error && <p>Error: {error.message}</p>}
    </form>
  );
}

export default CreateProjectForm;
```

### Step 6: Handle CORS (Backend Configuration)

If you're running React on a different port (e.g., `http://localhost:3000`), you'll need to configure CORS in your Django backend.

Add to your `settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ... other middleware
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Or allow all origins in development (not recommended for production)
# CORS_ALLOW_ALL_ORIGINS = True
```

Install django-cors-headers:

```bash
pip install django-cors-headers
```

---

## Complete Example: React Component with Multiple Queries

```javascript
import { useQuery, useMutation, gql } from '@apollo/client';
import { useState } from 'react';

const GET_PROJECT_STATISTICS = gql`
  query GetProjectStatistics($organizationId: Int!) {
    projectStatistics(organizationId: $organizationId) {
      totalProjects
      activeProjects
      completedProjects
      totalTasks
      completedTasks
      overallCompletionRate
    }
  }
`;

const GET_PROJECTS = gql`
  query GetProjectsByOrganization($organizationId: Int!) {
    projectsByOrganization(organizationId: $organizationId) {
      id
      name
      status
      taskCount
      completionRate
    }
  }
`;

const CREATE_TASK = gql`
  mutation CreateTask($input: TaskInput!) {
    createTask(input: $input) {
      success
      errors
      task {
        id
        title
        status
      }
    }
  }
`;

function Dashboard({ organizationId }) {
  const [selectedProjectId, setSelectedProjectId] = useState(null);
  
  // Fetch statistics
  const { data: statsData, loading: statsLoading } = useQuery(
    GET_PROJECT_STATISTICS,
    { variables: { organizationId: parseInt(organizationId) } }
  );

  // Fetch projects
  const { data: projectsData, loading: projectsLoading, refetch } = useQuery(
    GET_PROJECTS,
    { variables: { organizationId: parseInt(organizationId) } }
  );

  // Create task mutation
  const [createTask, { loading: creatingTask }] = useMutation(CREATE_TASK, {
    onCompleted: () => {
      refetch(); // Refresh projects list
    },
  });

  const handleCreateTask = (projectId, title) => {
    createTask({
      variables: {
        input: {
          projectId: parseInt(projectId),
          title,
          status: 'todo',
        },
      },
    });
  };

  if (statsLoading || projectsLoading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Dashboard</h1>
      
      {/* Statistics */}
      {statsData && (
        <div>
          <h2>Statistics</h2>
          <p>Total Projects: {statsData.projectStatistics.totalProjects}</p>
          <p>Active Projects: {statsData.projectStatistics.activeProjects}</p>
          <p>Completed Projects: {statsData.projectStatistics.completedProjects}</p>
          <p>Total Tasks: {statsData.projectStatistics.totalTasks}</p>
          <p>Completed Tasks: {statsData.projectStatistics.completedTasks}</p>
          <p>Overall Completion: {statsData.projectStatistics.overallCompletionRate}%</p>
        </div>
      )}

      {/* Projects List */}
      {projectsData && (
        <div>
          <h2>Projects</h2>
          {projectsData.projectsByOrganization.map((project) => (
            <div key={project.id} onClick={() => setSelectedProjectId(project.id)}>
              <h3>{project.name}</h3>
              <p>Status: {project.status}</p>
              <p>Tasks: {project.taskCount}</p>
              <p>Completion: {project.completionRate}%</p>
            </div>
          ))}
        </div>
      )}

      {/* Create Task Form */}
      {selectedProjectId && (
        <div>
          <h3>Create Task for Project {selectedProjectId}</h3>
          <button
            onClick={() => handleCreateTask(selectedProjectId, 'New Task')}
            disabled={creatingTask}
          >
            {creatingTask ? 'Creating...' : 'Create Task'}
          </button>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
```

---

## Testing Queries with GraphiQL

1. Start your Django development server:
   ```bash
   python manage.py runserver
   ```

2. Open your browser and navigate to: `http://localhost:8000/graphql/`

3. Use the GraphiQL interface to test queries interactively.

4. Example query to test:
   ```graphql
   query {
     projectsByOrganization(organizationId: 1) {
       id
       name
       status
       taskCount
     }
   }
   ```

---

## Error Handling

Always handle errors in your React components:

```javascript
const { loading, error, data } = useQuery(GET_PROJECTS, {
  variables: { organizationId },
  onError: (error) => {
    console.error('GraphQL Error:', error);
    // Show user-friendly error message
  },
});

if (error) {
  return (
    <div>
      <p>Error loading projects</p>
      <p>{error.message}</p>
    </div>
  );
}
```

---

## Notes

- **Date Format**: Use ISO 8601 format for dates (e.g., `"2024-12-31"` for dates, `"2024-12-31T23:59:59Z"` for datetimes)
- **Status Values**: Valid status values for projects: `"active"`, `"completed"`, `"on_hold"`
- **Task Status**: Valid status values for tasks: `"todo"`, `"in_progress"`, `"done"`
- **Organization ID**: All queries require a valid organization ID
- **Error Responses**: Mutations return `success` (boolean) and `errors` (array of strings) fields

---

## Additional Resources

- [Apollo Client Documentation](https://www.apollographql.com/docs/react/)
- [GraphQL Documentation](https://graphql.org/learn/)
- [Graphene Django Documentation](https://docs.graphene-python.org/projects/django/en/latest/)
