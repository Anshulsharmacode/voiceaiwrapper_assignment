import React, { useState } from 'react';

interface OrganizationFormProps {
  isOpen: boolean;
  onClose: () => void;
  onCreated: (organization: { id: number; name: string; contact_email: string; slug: string | null }) => void;
}

const BACKEND_BASE_URL =
  import.meta.env.VITE_BACKEND_BASE_URL ||
  (import.meta.env.VITE_GRAPHQL_ENDPOINT
    ? import.meta.env.VITE_GRAPHQL_ENDPOINT.replace(/\/graphql\/?$/, '')
    : 'http://localhost:8000');

const OrganizationForm: React.FC<OrganizationFormProps> = ({ isOpen, onClose, onCreated }) => {
  const [name, setName] = useState('');
  const [contactEmail, setContactEmail] = useState('');
  const [slug, setSlug] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const reset = () => {
    setName('');
    setContactEmail('');
    setSlug('');
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${BACKEND_BASE_URL}/api/organizations/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          contact_email: contactEmail,
          slug: slug || undefined,
        }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        const message =
          data?.error ||
          (data?.errors && JSON.stringify(data.errors)) ||
          'Failed to create organization';
        throw new Error(message);
      }

      onCreated(data.data);
      reset();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Something went wrong while creating organization');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md">
        <div className="flex justify-between items-center px-6 py-4 border-b">
          <h2 className="text-lg sm:text-xl font-bold text-gray-900">Create Organization</h2>
          <button
            type="button"
            onClick={() => {
              reset();
              onClose();
            }}
            className="text-gray-400 hover:text-gray-600 text-2xl leading-none"
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="px-6 py-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Name *
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Acme Inc."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Contact Email *
            </label>
            <input
              type="email"
              value={contactEmail}
              onChange={(e) => setContactEmail(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="admin@acme.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Slug (optional)
            </label>
            <input
              type="text"
              value={slug}
              onChange={(e) => setSlug(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="acme-inc"
            />
            <p className="mt-1 text-xs text-gray-500">
              If left empty, the slug will be generated from the name.
            </p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 text-sm px-3 py-2 rounded-lg">
              {error}
            </div>
          )}

          <div className="flex gap-3 pt-2 pb-1">
            <button
              type="button"
              onClick={() => {
                reset();
                onClose();
              }}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm sm:text-base"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 text-sm sm:text-base"
            >
              {loading ? 'Creating...' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default OrganizationForm;


