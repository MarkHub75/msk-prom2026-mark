import type { FormEvent, ReactNode } from "react";

export function Modal({
  title,
  onClose,
  children,
}: {
  title: string;
  onClose: () => void;
  children: ReactNode;
}) {
  return (
    <div className="modal-backdrop">
      <div className="modal" role="dialog" aria-modal="true" aria-label={title}>
        <header className="modal-header">
          <h2>{title}</h2>
          <button type="button" onClick={onClose} aria-label="Закрыть">
            ×
          </button>
        </header>
        {children}
      </div>
    </div>
  );
}

export function FormField({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="form-field">
      <span>{label}</span>
      {children}
    </label>
  );
}

// A modal form: the API error text is shown right above the buttons (tech.md 8.14).
export function FormModal({
  title,
  error,
  submitText,
  onSubmit,
  onClose,
  children,
}: {
  title: string;
  error: string | undefined;
  submitText: string;
  onSubmit: () => void;
  onClose: () => void;
  children: ReactNode;
}) {
  const submit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit();
  };
  return (
    <Modal title={title} onClose={onClose}>
      <form onSubmit={submit}>
        {children}
        {error && (
          <p className="form-error" role="alert">
            {error}
          </p>
        )}
        <div className="form-buttons">
          <button type="submit">{submitText}</button>
          <button type="button" onClick={onClose}>
            Отмена
          </button>
        </div>
      </form>
    </Modal>
  );
}

export function ConfirmDialog({
  text,
  error,
  onConfirm,
  onClose,
}: {
  text: string;
  error: string | undefined;
  onConfirm: () => void;
  onClose: () => void;
}) {
  return (
    <FormModal
      title="Подтвердите действие"
      error={error}
      submitText="Удалить"
      onSubmit={onConfirm}
      onClose={onClose}
    >
      <p>{text}</p>
    </FormModal>
  );
}
