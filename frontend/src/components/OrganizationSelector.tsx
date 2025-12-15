import React, { useEffect, useState } from 'react';
import OrganizationForm from './OrganizationForm';

interface Organization {
  id: number;
  name: string;
  slug: string | null;
  contact_email: string;
}

interface OrganizationSelectorProps {
  value: number | null;
  onChange: (organizationId: number) => void;
}

const BACKEND_BASE_URL =
  import.meta.env.VITE_BACKEND_BASE_URL ||
  (import.meta.env.VITE_GRAPHQL_ENDPOINT
    ? import.meta.env.VITE_GRAPHQL_ENDPOINT.replace(/\/graphql\/?$/, '')
    : 'http://localhost:8000');

const OrganizationSelector: React.FC<OrganizationSelectorProps> = ({ value, onChange }) => {
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);

  useEffect(() => {
    const fetchOrganizations = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`${BACKEND_BASE_URL}/api/organizations/`);
        const data = await response.json();

        if (!response.ok || !data.success) {
          const message = data?.error || 'Failed to load organizations';
          throw new Error(message);
        }

        setOrganizations(data.data || []);

        if (!value && data.data && data.data.length > 0) {
          onChange(data.data[0].id);
        }
      } catch (err: any) {
        setError(err.message || 'Error loading organizations');
      } finally {
        setLoading(false);
      }
    };

    fetchOrganizations();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleCreated = (org: Organization) => {
    setOrganizations((prev) => [...prev, org]);
    onChange(org.id);
  };

  return (
    <div className="w-full flex flex-col gap-2 sm:flex-row sm:items-center">
      <div className="flex-1">
        <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1">
          Organization
        </label>
        <div className="flex gap-2">
          <select
            value={value || ''}
            onChange={(e) => {
              const id = Number(e.target.value);
              if (id) onChange(id);
            }}
            className="flex-1 min-w-0 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            disabled={loading || organizations.length === 0}
          >
            {loading && <option value="">Loading organizations...</option>}
            {!loading && organizations.length === 0 && (
              <option value="">No organizations. Create one to get started.</option>
            )}
            {!loading &&
              organizations.length > 0 && (
                <>
                  <option value="">Select organization</option>
                  {organizations.map((org) => (
                    <option key={org.id} value={org.id}>
                      {org.name} (#{org.id})
                    </option>
                  ))}
                </>
              )}
          </select>
        </div>
        {error && (
          <p className="mt-1 text-xs text-red-600">
            {error}
          </p>
        )}
      </div>

      <button
        type="button"
        onClick={() => setShowCreateModal(true)}
        className="mt-1 sm:mt-6 inline-flex items-center justify-center px-3 py-2 border border-blue-600 text-xs sm:text-sm font-medium rounded-lg text-blue-600 bg-white hover:bg-blue-50 whitespace-nowrap"
      >
        + New Org
      </button>

      <OrganizationForm
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onCreated={handleCreated}
      />
    </div>
  );
};

export default OrganizationSelector;


