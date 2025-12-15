import React, { createContext, type ReactNode, useContext } from "react";
import {
  ApolloClient,
  InMemoryCache,
  gql,
} from "@apollo/client";
import { HttpLink } from "@apollo/client/link/http";
import { ApolloProvider, useMutation, useQuery } from "@apollo/client/react";

const GRAPHQL_ENDPOINT =
  import.meta.env.VITE_GRAPHQL_ENDPOINT ||"https://voiceaiwrapper-assignment.onrender.com" || "http://localhost:8000/graphql/";

const httpLink = new HttpLink({
  uri: GRAPHQL_ENDPOINT,
});

const client = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
});

// GraphQL Queries
export const GET_PROJECTS_BY_ORGANIZATION = gql`
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

export const GET_PROJECT_STATISTICS = gql`
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
`;

export const GET_PROJECT = gql`
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
    }
  }
`;

export const GET_TASKS_BY_PROJECT = gql`
  query GetTasksByProject($projectId: Int!) {
    tasksByProject(projectId: $projectId) {
      id
      title
      description
      status
      assigneeEmail
      dueDate
      createdAt
      commentCount
    }
  }
`;

export const GET_TASK = gql`
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
      comments {
        id
        content
        authorEmail
        timestamp
      }
    }
  }
`;

// GraphQL Mutations
export const CREATE_PROJECT = gql`
  mutation CreateProject($input: ProjectInput!) {
    createProject(input: $input) {
      project {
        id
        name
        description
        status
        dueDate
        createdAt
      }
      success
      errors
    }
  }
`;

export const UPDATE_PROJECT = gql`
  mutation UpdateProject($projectId: Int!, $input: ProjectUpdateInput!) {
    updateProject(projectId: $projectId, input: $input) {
      project {
        id
        name
        description
        status
        dueDate
        createdAt
      }
      success
      errors
    }
  }
`;

export const CREATE_TASK = gql`
  mutation CreateTask($input: TaskInput!) {
    createTask(input: $input) {
      task {
        id
        title
        description
        status
        assigneeEmail
        dueDate
        createdAt
      }
      success
      errors
    }
  }
`;

export const UPDATE_TASK = gql`
  mutation UpdateTask($taskId: Int!, $input: TaskUpdateInput!) {
    updateTask(taskId: $taskId, input: $input) {
      task {
        id
        title
        description
        status
        assigneeEmail
        dueDate
        createdAt
      }
      success
      errors
    }
  }
`;

export const ADD_TASK_COMMENT = gql`
  mutation AddTaskComment($input: TaskCommentInput!) {
    addTaskComment(input: $input) {
      comment {
        id
        content
        authorEmail
        timestamp
      }
      success
      errors
    }
  }
`;


interface GraphQLContextType {
  getProjectsByOrganization: (organizationId: number) => any;
  getProjectStatistics: (organizationId: number) => any;
  getProject: (projectId: number) => any;
  getTasksByProject: (projectId: number) => any;
  getTask: (taskId: number) => any;
  createProject: (input: any) => any;
  updateProject: (projectId: number, input: any) => any;
  createTask: (input: any) => any;
  updateTask: (taskId: number, input: any) => any;
  addTaskComment: (input: any) => any;
}

const GraphQLContext = createContext<GraphQLContextType | undefined>(undefined);

export const GraphQLProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <ApolloProvider client={client}>
      {children}
    </ApolloProvider>
  );
};

export const useGraphQL = () => {
  const context = useContext(GraphQLContext);
  if (!context) {
    throw new Error('useGraphQL must be used within GraphQLProvider');
  }
  return context;
};

export const useProjectsByOrganization = (organizationId: number) => {
  return useQuery(GET_PROJECTS_BY_ORGANIZATION, {
    variables: { organizationId },
    skip: !organizationId,
  });
};

export const useProjectStatistics = (organizationId: number) => {
  return useQuery(GET_PROJECT_STATISTICS, {
    variables: { organizationId },
    skip: !organizationId,
  });
};

export const useProject = (projectId: number) => {
  return useQuery(GET_PROJECT, {
    variables: { projectId },
    skip: !projectId,
  });
};

export const useTasksByProject = (projectId: number) => {
  return useQuery(GET_TASKS_BY_PROJECT, {
    variables: { projectId },
    skip: !projectId,
  });
};

export const useTask = (taskId: number) => {
  return useQuery(GET_TASK, {
    variables: { taskId },
    skip: !taskId,
  });
};

export const useCreateProject = () => {
  return useMutation(CREATE_PROJECT, {
    refetchQueries: ['GetProjectsByOrganization', 'GetProjectStatistics'],
  });
};

export const useUpdateProject = () => {
  return useMutation(UPDATE_PROJECT, {
    refetchQueries: ['GetProjectsByOrganization', 'GetProject'],
  });
};

export const useCreateTask = () => {
  return useMutation(CREATE_TASK, {
    refetchQueries: ['GetProject', 'GetTask', 'GetTasksByProject'],
  });
};

export const useUpdateTask = () => {
  return useMutation(UPDATE_TASK, {
    refetchQueries: ['GetTask', 'GetProject', 'GetTasksByProject'],
  });
};

export const useAddTaskComment = () => {
  return useMutation(ADD_TASK_COMMENT, {
    refetchQueries: ['GetTask'],
  });
};

// // Export useQuery and useMutation from Apollo for custom queries
// export { useQuery, useMutation } from '@apollo/client';
// export { client };
